class StackRequestError(IOError):
    """Raise exception when an error occurred when making a request to the StackExchange API"""


class ZeroSearchResultsError(RuntimeError):
    """Raise exception when a stack exchange request yields zero search results"""


class RedisConnectionError(ConnectionError):
    """Raise exception when connection to a Redis DB fails"""
