from .fixtures import (cached_stack_exchange,
                       error_stack_exchange_http_response, search_request,
                       stack_exchange)


def test_stack_exchange_search(stack_exchange, search_request):
    search_results = stack_exchange.search(search_request)
    assert len(search_results) == 2


def cached_stack_exchange_search(cached_stack_exchange):
    pass


def test_get_request_stack_request_error(error_stack_exchange_http_response):
    pass


def test_zero_search_results_error():
    pass


def test_get_questions():
    pass


def test_get_answers():
    pass
