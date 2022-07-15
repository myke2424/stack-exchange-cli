import pytest

from stack_exchange.cache import Cache
from stack_exchange.models import Answer, Question, SearchRequest, SearchResult
from stack_exchange.search import Searchable


class TestCache(Cache):
    """In memory dict to simulate a cache"""

    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value


class TestStackExchangeClient(Searchable):
    def search(self, request: SearchRequest) -> list[SearchResult]:
        """Test search interface for stack-exchange"""
        questions = [
            Question(
                body="Question body 1",
                score=50,
                creation_date=1,
                title="Question title 1",
                link="stackexchange.com/1",
                accepted_answer_id=1,
            ),
            Question(
                body="Question body 2",
                score=10,
                creation_date=2,
                title="Question title 2",
                link="stackexchange.com/2",
                accepted_answer_id=2,
            ),
        ]
        answers = [
            Answer(body="Answer for question 1", score=100, creation_date=1, is_accepted=True),
            Answer(body="Answer for question ", score=200, creation_date=2, is_accepted=True),
        ]
        return [SearchResult(question, answer) for (question, answer) in zip(questions, answers)]


@pytest.fixture
def search_request():
    request = (
        SearchRequest.Builder("Reverse a linked-list", "stackoverflow")
        .with_tags("python")
        .accepted_only()
        .n_results(10)
        .build()
    )
    return request


@pytest.fixture
def stack_exchange():
    return TestStackExchangeClient()


@pytest.fixture
def cache():
    return TestCache()


@pytest.fixture
def error_stack_exchange_http_response():
    return {"error_id": 502, "error_message": "too many requests from this IP", "error_name": "throttle_violation"}