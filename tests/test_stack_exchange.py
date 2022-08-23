from unittest.mock import MagicMock, Mock, patch

import pytest

from stack_exchange import exceptions
from stack_exchange.models import Answer, Question, SearchResult
from stack_exchange.search import StackExchange

from .fixtures import (
    cached_stack_exchange_obj,
    search_request,
    search_results_list,
    stack_exchange_obj,
    stack_get_answers_response,
    stack_search_response,
)


@patch("stack_exchange.search.requests", autospec=True)
def test_search_invalid_get_requests_raises_stack_request_exception(mock_requests, search_request):
    se = StackExchange()
    mock_response = MagicMock(status_code=404)
    mock_response.json.return_value = {
        "error_id": 404,
        "error_message": "no method found with this name",
        "error_name": "no_method",
    }

    mock_requests.get.return_value = mock_response

    with pytest.raises(exceptions.StackRequestError):
        se.search(search_request)


@pytest.mark.parametrize("num, questions_expected_len", [(5, 5), (10, 10), (1, 1)])
def test_get_questions(stack_exchange_obj, num, questions_expected_len, stack_search_response):
    """Tests get questions builds a list of question objects of length num"""
    questions = stack_exchange_obj._get_questions(search_params={"q": "DFS vs BFS", "site": "stackoverflow"}, num=num)

    assert len(questions) == questions_expected_len
    assert all(isinstance(q, Question) for q in questions)


def test_get_answers_from_questions(stack_exchange_obj, stack_search_response, stack_get_answers_response):
    """Tests getting list of answers from a list of questions and a given site"""
    questions = stack_exchange_obj._get_questions(search_params={"q": "DFS vs BFS", "site": "stackoverflow"}, num=10)
    answers = stack_exchange_obj._get_accepted_answers_for_questions(questions, site="stackoverflow")

    assert len(answers) == len(questions)
    assert all(isinstance(a, Answer) for a in answers)


def test_search(stack_exchange_obj, search_request, stack_search_response, stack_get_answers_response):
    """Tests stack exchange search returns a list of search results with expected attributes"""
    search_results = stack_exchange_obj.search(search_request)

    assert all(isinstance(sr, SearchResult) for sr in search_results)
    assert all(hasattr(sr, "question") for sr in search_results)
    assert all(hasattr(sr, "answer") for sr in search_results)

    question_accepted_answer_ids = [sr.question.accepted_answer_id for sr in search_results]
    answer_ids = [sr.answer.answer_id for sr in search_results]

    assert question_accepted_answer_ids == answer_ids


def test_cached_search_cache_hit(cached_stack_exchange_obj, search_request, search_results_list):
    """Tests the results are fetched from the cache for the same request instead of making repeated API called to stack-exchange"""

    # mock stack exchange search api call
    cached_stack_exchange_obj.service.search = Mock(return_value=search_results_list)

    for _ in range(10):
        cached_stack_exchange_obj.search(search_request)

    # assert stack api service is only called ONCE for the same request
    cached_stack_exchange_obj.service.search.assert_called_once()


def test_cached_search(cached_stack_exchange_obj, search_request, stack_search_response, stack_get_answers_response):
    """Tests caching proxy objects caches search request and returns it for subsequent calls"""
    # unique request url used for our search and stored in the cache as the key
    request_url = "https://api.stackexchange.com/2.3/search/advanced?q=DFS+vs+BFS&site=stackoverflow&accepted=True&filter=withbody&sort=votes"
    search_results = cached_stack_exchange_obj.search(search_request)
    cached_search_results = cached_stack_exchange_obj.search(search_request)

    assert search_results == cached_search_results
    assert cached_stack_exchange_obj.cache.get(request_url) is not None


def test_search_results_serialization_and_deserialization(search_results_list):
    """Test search results serialization to json and deserialization - used for cache saves and hits"""
    search_results_json = [sr.to_json() for sr in search_results_list]
    assert all(isinstance(sr_json, dict) for sr_json in search_results_json)

    search_results_deserialized = [SearchResult.from_json(sr_json) for sr_json in search_results_json]
    assert all(isinstance(sr, SearchResult) for sr in search_results_deserialized)
