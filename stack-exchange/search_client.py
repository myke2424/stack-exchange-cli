"""
Stack exchange client interface used for searching!
"""

import requests
from dataclasses import dataclass
from .errors import StackRequestError, ZeroSearchResultsError
from typing import Optional, List


@dataclass(frozen=True)
class SearchResult:
    question_title: str
    question_body: str
    answer: str
    is_answered: bool
    creation_date: str
    score: int

    @classmethod
    def from_raw_response(cls, search_response: dict, answer: str) -> 'SearchResult':
        r = search_response
        return cls(question_title=r['title'], question_body=r['body'], answer=answer, is_answered=r['is_answered'],
                   creation_date=r['creation_date'], score=r['score'])


class StackExchange:
    """
    Wrapper class for the stack exchange API
    Facade only caring about search
    """

    SEARCH_ENDPOINT = "/search/advanced"

    def __init__(self, version: str = "2.3") -> None:
        self.__version = version
        self.__url = f"https://api.stackexchange.com/{version}"

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """ Make a GET request to the given stack exchange endpoint with the provided query params """
        url = self.__url + endpoint
        response = requests.get(url, params)
        response_dict = response.json()

        if response_dict.get('error_message') is not None:
            raise StackRequestError(f"Request FAILED to url: {response.url} \n Error: {response_dict['error_message']}")
        return response_dict

    # Refactor search to use kwargs or config object?
    # Inbody = the query string is found in the text body
    def search(self, query: str, params: dict = Optional[None], site: str = "stackoverflow", answers: int = 1,
               accepted: bool = True, in_body: bool = False, tags: Optional[List[str]] = None,
               sort: str = "votes") -> str:
        params = {"accepted": accepted, "filter": "withbody", "site": site, "answers": answers, "sort": sort}

        if in_body:
            # query string must be in body of text
            params.update({"body": query})

        # semi colon delimited list of tags, at least one has to be present resutls
        if tags is not None:
            params.update({"tagged": tags})
            del params['q']  # remove query since we're searching by body... which makes more sense i think!

        response = self._make_request(endpoint=self.SEARCH_ENDPOINT, params=params)

        if not response['items']:
            raise ZeroSearchResultsError("No search results found.")

        answer_id = response['items'][0]['accepted_answer_id']

        answer = self._make_request(f"/answers/{answer_id}", params={"site": site,
                                                                     "filter": "withbody"})
        search_result = SearchResult.from_raw_response(response['items'][0], answer['items'][0]['body'])

        return search_result

        # res = resp['items'][0]
        # print(res['title'])
    #  question = res['body']
    # console.print(strip_tags(question))
    #

    #
    # print("***ANSWER*** \n")
    # a = answer['items'][0]['body']
    # # console.print(strip_tags(a))
