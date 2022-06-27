class StackRequestError(IOError):
    """ Raise exception when an error occurred when making a request to the StackExchange API """


class ZeroSearchResultsError(RuntimeError):
    """ Raise exception when a stack exchange request responds with zero search results """
