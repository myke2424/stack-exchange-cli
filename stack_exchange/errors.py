"""
Module contains custom Exceptions used throughout the application for more fine-grained error messages and tracebacks.
"""

class StackRequestError(IOError):
    """Raise exception when an error occurred when making a request to the StackExchange API"""


class ZeroSearchResultsError(RuntimeError):
    """Raise exception when a stack exchange request yields zero search results"""


class RedisConnectionError(ConnectionError):
    """Raise exception when connection to a Redis DB fails"""


class InvalidConfigurationError(ValueError):
    """Raise when user uses an invalid config.yaml file"""
