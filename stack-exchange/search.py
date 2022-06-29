"""
Stack exchange client interface used for searching!
"""

import requests
from .errors import StackRequestError, ZeroSearchResultsError
from .models import Question, Answer, SearchParams, SearchResult
from typing import Optional, List
from abc import ABC, abstractmethod
from .cache import Cache


class SearchClient(ABC):
    @abstractmethod
    def search(
        self,
        query: str,
        count: int,
        tags: List[str],
        site: str,
        in_body: bool = False,
    ):
        pass


class StackExchange(SearchClient):
    """
    Wrapper class for the stack exchange API
    Facade only caring about search
    """

    SEARCH_ENDPOINT = "/search/advanced"
    ANSWERS_ENDPOINT = "/answers"

    def __init__(self, version: str = "2.3") -> None:
        self.__version = version
        self.url = f"https://api.stackexchange.com/{version}"

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """Make a GET request to the given stack exchange endpoint with the provided query params"""
        url = self.url + endpoint
        response = requests.get(url, params)
        response_dict = response.json()

        if response_dict.get("error_message") is not None:
            raise StackRequestError(f"Request FAILED to url: {response.url} \n Error: {response_dict['error_message']}")
        return response_dict

    def _get_search_advanced(self, params: dict) -> dict:
        """GET /search/advanced. Read more: https://api.stackexchange.com/docs/advanced-search"""
        search_response = self._make_request(endpoint=self.SEARCH_ENDPOINT, params=params)

        if not search_response["items"]:
            raise ZeroSearchResultsError("No search results found.")

        return search_response

    def _get_answers(self, ids: List[str], params: dict) -> dict:
        """GET /answers/{ids}. Semi-colon delimited Ids, Read more: https://api.stackexchange.com/docs/answers-by-ids"""
        return self._make_request(endpoint=f"{self.ANSWERS_ENDPOINT}/{';'.join(ids)}", params=params)

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
    Proxy structural design pattern. This class uses an identical search interface to StackExchange
    Use a cache as a proxy object to set and get search results for faster look up time.
    """

    def __init__(self, stack_exchange_service: StackExchange, cache: Cache) -> None:
        self.cache = cache
        self.service = stack_exchange_service

    def search(
        self,
        query: str,
        count: int = 1,
        tags: Optional[List[str]] = None,
        site: str = "stackoverflow",
        in_body: bool = False,
    ):
        search_params = self.service._build_search_params(query, count, tags, site, in_body)
        request = requests.Request(
            method="GET", url=f"{self.service.url}{self.service.SEARCH_ENDPOINT}", params=search_params
        ).prepare()

        # Cache the request url!
        print(f"URL: {request.url}")

        cached = self.cache.get(request.url)

        if cached is not None:
            print("Fetching result from cache!")
            return SearchResult(**cached)

        search_results = self.service.search(query, count, tags, site, in_body)
        self.cache.set(key=request.url, value=search_results[0].__dict__)

        return search_results[0]
