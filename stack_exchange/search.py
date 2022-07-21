"""
Module contains the main API code for searching stack-exchange websites.
Includes a stack-exchange wrapper class used for searching, as well as a
proxy cache class, used for searching and caching the results of each search.
"""


import json
import logging
from abc import ABC, abstractmethod

import requests

from .cache import Cache
from .errors import StackRequestError, ZeroSearchResultsError
from .models import Answer, Question, SearchRequest, SearchResult, StackExchangeApiConfig

logger = logging.getLogger(__name__)


class Searchable(ABC):
    @abstractmethod
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Main interface used for searching a stack exchange website."""


class StackExchange(Searchable):
    """Wrapper class for the Stack Exchange API used for searching only"""

    _SEARCH_ENDPOINT = "/search/advanced"
    _ANSWERS_ENDPOINT = "/answers"

    def __init__(self, api_config: StackExchangeApiConfig | None = None) -> None:
        self.__version = api_config.version if api_config else "2.3"
        self.__api_config = api_config
        self.url = f"https://api.stackexchange.com/{self.__version}"

    @property
    def search_url(self):
        return self.url + self._SEARCH_ENDPOINT

    @property
    def answers_url(self):
        return self.url + self._ANSWERS_ENDPOINT

    def _make_get_request(self, url: str, params: dict) -> dict:
        """Make a GET request to the given stack exchange endpoint with the provided query params"""
        logger.debug(f"Making GET request to: {url}: \n params={json.dumps(params, indent=2)}")

        # Use key to receive a higher request quota
        if self.__api_config is not None and self.__api_config.api_key:
            params["key"] = self.__api_config.api_key

        response = requests.get(url, params)
        response_dict = response.json()
        logger.debug(f"Made request to: {response.url}")

        if response_dict.get("error_message") is not None:
            raise StackRequestError(
                f"Request FAILED to url: {response.url} \nResponse Error Message: {response_dict['error_message']}"
            )
        return response_dict

    def _get_search_advanced(self, params: dict) -> dict:
        """GET /search/advanced. Read more: https://api.stackexchange.com/docs/advanced-search"""
        search_response = self._make_get_request(url=self.search_url, params=params)

        if not search_response["items"]:
            raise ZeroSearchResultsError("No search results found.")

        return search_response

    def _get_answers(self, ids: list[str], params: dict) -> dict:
        """GET /answers/{ids}. Semicolon delimited Ids, Read more: https://api.stackexchange.com/docs/answers-by-ids"""
        return self._make_get_request(url=f"{self.answers_url}/{';'.join(ids)}", params=params)

    def _get_questions(self, search_params: dict, num: int) -> list[Question]:
        """Get a list of questions by making a request to /search/advanced with the given search_params"""
        search_response = self._get_search_advanced(search_params)
        # We only care about the first 'n' results
        questions = [Question.from_response_item(item) for item in search_response["items"][:num]]

        return questions

    def _get_accepted_answers_for_questions(self, questions: list[Question], site: str) -> list[Answer]:
        """Get the top accepted answer for each question by making a request to /answers/{ids}"""
        accepted_answer_ids = [str(question.accepted_answer_id) for question in questions]
        answers_response = self._get_answers(
            accepted_answer_ids, params={"site": site, "filter": "withbody"}  # withbody gives us the answer body
        )
        answers = [Answer.from_response_item(item) for item in answers_response["items"]]

        return answers

    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Search stack exchange"""
        questions = self._get_questions(request.to_json(), request.num)
        answers = self._get_accepted_answers_for_questions(questions, request.site)

        search_results = [SearchResult(q, a) for q in questions for a in answers if q.accepted_answer_id == a.answer_id]
        return search_results


class CachedStackExchange(Searchable):
    """
    Proxy structural design pattern.
    Use a cache as a proxy object to set and get search results for faster look up time.
    """

    def __init__(self, stack_exchange_service: StackExchange, cache: Cache, overwrite: bool = False) -> None:
        self.cache = cache
        self.service = stack_exchange_service
        self._overwrite = overwrite

    def _prepare_search_uri(self, search_params: dict) -> str:
        """Prepare the search url to use it for the key when caching requests"""
        request = requests.Request(method="GET", url=self.service.search_url, params=search_params).prepare()
        return request.url

    def search(self, request: SearchRequest) -> list[SearchResult]:
        """
        Same interface for searching as the StackExchange service.
        Check for cached request value, return value if cache hit, otherwise invoke search on stack exchange service
        and return results
        """
        request_url = self._prepare_search_uri(request.to_json())

        cached_search_results = self.cache.get(request_url)

        if cached_search_results is not None and not self._overwrite:
            logger.info(f"Using cached results for url: {request_url}")
            return [SearchResult.from_json(sr_json) for sr_json in cached_search_results]

        search_results = self.service.search(request)
        search_results_json = [sr.to_json() for sr in search_results]

        # cache request URI as the key and serialized JSON list of search results the value.
        self.cache.set(key=request_url, value=search_results_json)

        return search_results
