from .fixtures import (error_stack_exchange_http_response, search_request,
                       stack_exchange)


def test_search(stack_exchange, search_request):
    search_results = stack_exchange.search(search_request)
    assert len(search_results) == 2


def test_get_request_stack_request_error(error_stack_exchange_http_response):
    pass


def test_zero_search_results_error():
    pass


def test_get_questions():
    pass


def test_get_answers():
    pass
