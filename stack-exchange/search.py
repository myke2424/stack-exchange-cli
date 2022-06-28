"""
Stack exchange client interface used for searching!
"""
import json

import requests
from dataclasses import dataclass
from .errors import StackRequestError, ZeroSearchResultsError
from typing import Optional, List
from abc import ABC, abstractmethod
from .cache import Cache


@dataclass(frozen=True)
class SearchResult:
    question_title: str
    question_body: str
    question_score: int
    creation_date: str
    answer: str
    answer_score: int

    @classmethod
    def from_search_and_answer_response(cls, search_response: dict, answer_response: dict) -> "SearchResult":
        return cls(
            question_title=search_response["title"],
            question_body=search_response["body"],
            question_score=search_response["score"],
            creation_date=search_response["creation_date"],
            answer=answer_response["body"],
            answer_score=answer_response["score"],
        )


# Impelement searchable!?
class StackExchange:
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
        return self._make_request(endpoint=self.SEARCH_ENDPOINT, params=params)

    # TODO: Update this so we take a delmited list of ids... so we make 1 request instead of n requests.
    def _get_answer(self, id_: int, params: dict) -> dict:
        """GET /answers/{ids}. Read more: https://api.stackexchange.com/docs/answers-by-ids"""
        return self._make_request(endpoint=f"{self.ANSWERS_ENDPOINT}/{id_}", params=params)

    def _build_search_params(
            self,
            query: str,
            count: int = 1,
            tags: Optional[List[str]] = None,
            site: str = "stackoverflow",
            in_body: bool = False,
    ) -> dict:
        """Build parameter dictionary for search requests"""
        params = {
            "q": query,
            "accepted": True,
            "filter": "withbody",
            "site": site,
            "sort": "votes",
            "answers": count,
        }

        if in_body:
            params["body"] = query
            del params["q"]  # remove query since we're searching by body

        if tags is not None:
            params["tagged"] = ";".join(tags)

        return params

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
        search_params = self._build_search_params(query, count, tags, site, in_body)
        search_response = self._get_search_advanced(search_params)

        if not search_response["items"]:
            raise ZeroSearchResultsError("No search results found.")

        # We only care about the first 'n' results, where n is the count param
        questions = search_response["items"][:count]

        answers = [
            self._get_answer(id_=item["accepted_answer_id"], params={"site": site, "filter": "withbody"})["items"][0]
            for item in questions
        ]

        return [
            SearchResult.from_search_and_answer_response(question, answer)
            for (question, answer) in zip(questions, answers)
        ]


class CachedStackExchange:
    """
    Proxy design pattern. This class uses an identical search interface to StackExchange
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
        if self.cache.get(request.url) is not None:
            print("Fetching result from cache!")
            return SearchResult(**self.cache.get(request.url))

        search_results = self.service.search(query, count, tags, site, in_body)
        self.cache.set(key=request.url, value=search_results[0].__dict__)

        return search_results[0]
