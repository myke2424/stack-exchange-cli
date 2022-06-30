"""
Stack exchange client interface used for searching!
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import List, Optional

import requests

from .cache import Cache
from .errors import StackRequestError, ZeroSearchResultsError
from .models import Answer, Question, SearchParams, SearchResult

logger = logging.getLogger(__name__)


class SearchClient(ABC):
    @abstractmethod
    def search(
        self,
        query: str,
        count: int,
        tags: Optional[List[str]],
        site: str,
        in_body: bool = False,
    ) -> List[SearchResult]:
        pass


class StackExchange(SearchClient):
    """Wrapper class for the Stack Exchange API used for Search Only"""

    _SEARCH_ENDPOINT = "/search/advanced"
    _ANSWERS_ENDPOINT = "/answers"

    def __init__(self, version: str = "2.3") -> None:
        self.__version = version
        self.url = f"https://api.stackexchange.com/{version}"

    @property
    def search_url(self):
        return self.url + self._SEARCH_ENDPOINT

    @property
    def answers_url(self):
        return self.url + self._ANSWERS_ENDPOINT

    @staticmethod
    def _make_get_request(url: str, params: dict) -> dict:
        """Make a GET request to the given stack exchange endpoint with the provided query params"""
        logger.debug(f"Making GET request to: {url}: \n params={json.dumps(params, indent=2)}")

        response = requests.get(url, params)
        response_dict = response.json()

        if response_dict.get("error_message") is not None:
            raise StackRequestError(f"Request FAILED to url: {response.url} \n Error: {response_dict['error_message']}")
        return response_dict

    def _get_search_advanced(self, params: dict) -> dict:
        """GET /search/advanced. Read more: https://api.stackexchange.com/docs/advanced-search"""
        search_response = self._make_get_request(url=self.search_url, params=params)

        if not search_response["items"]:
            raise ZeroSearchResultsError("No search results found.")

        return search_response

    def _get_answers(self, ids: List[str], params: dict) -> dict:
        """GET /answers/{ids}. Semi-colon delimited Ids, Read more: https://api.stackexchange.com/docs/answers-by-ids"""
        return self._make_get_request(url=f"{self.answers_url}/{';'.join(ids)}", params=params)

    def _get_questions(self, search_params: SearchParams) -> List[Question]:
        """
        Get a list of questions by making a request to /search/advanced with the given search_params
        """

        search_response = self._get_search_advanced(search_params.to_json())

        # We only care about the first 'n' results, where n is the count param
        questions = [
            Question.from_search_response_item(item) for item in search_response["items"][: search_params.count]
        ]

        return questions

    def _get_accepted_answers(self, questions: List[Question], site: str) -> List[Answer]:
        """Get the top accepted answer for each question by making a request to /answers/{ids}"""
        accepted_answer_ids = [str(question.accepted_answer_id) for question in questions]
        answers_response = self._get_answers(
            accepted_answer_ids, params={"site": site, "filter": "withbody"}  # withbody gives us the answer body
        )
        answers = [Answer.from_answer_response_item(item) for item in answers_response["items"]]

        return answers

    def search(
        self,
        query: str,
        count: int = 1,
        tags: Optional[List[str]] = None,
        site: str = "stackoverflow",
        in_body: bool = False,
    ) -> List[SearchResult]:
        """
        Main interface used for searching stack exchange.

        :param query: Search query to search for on stack exchange
        :param count: Number of results we want, default to 1
        :param tags: Search tags, i.e. ['python', 'recursion']
        :param site: Stack exchange website, i.e. 'stackoverflow', 'askubuntu', 'softwareengineering'
        :param in_body: Query string must be present in body of post
        :return: Search Result
        """
        search_params = SearchParams(query, count, tags, site, in_body)

        questions = self._get_questions(search_params)
        answers = self._get_accepted_answers(questions, site)

        return [SearchResult(question, answer) for (question, answer) in zip(questions, answers)]


class CachedStackExchange(SearchClient):
    """
    Proxy structural design pattern. Use a cache as a proxy object to set and get search results for faster look up time.
    """

    def __init__(self, stack_exchange_service: StackExchange, cache: Cache) -> None:
        self.cache = cache
        self.service = stack_exchange_service

    def _prepare_search_url(self, search_params: SearchParams) -> str:
        """Prepare the search url to use it for the key when caching requests"""
        request = requests.Request(method="GET", url=self.service.search_url, params=search_params.to_json()).prepare()
        return request.url

    def search(
        self,
        query: str,
        count: int = 1,
        tags: Optional[List[str]] = None,
        site: str = "stackoverflow",
        in_body: bool = False,
    ) -> List[SearchResult]:
        search_params = SearchParams(query, count, tags, site, in_body)
        request_url = self._prepare_search_url(search_params)

        cached_search_results = self.cache.get(request_url)

        if cached_search_results is not None:
            logger.info(f"Using cached results for url: {request_url}")
            return [SearchResult.from_json(sr_json) for sr_json in cached_search_results]

        search_results = self.service.search(query, count, tags, site, in_body)
        search_results_dict = [sr.to_json() for sr in search_results]

        self.cache.set(key=request_url, value=search_results_dict)

        return search_results
