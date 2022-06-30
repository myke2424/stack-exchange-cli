import logging
from typing import Optional

import utils

from .cache import RedisCache
from .commands import get_cmd_args
from .search import CachedStackExchange, StackExchange

logger = logging.getLogger(__name__)
logger.addHandler()

# TODO: Implement Chain of Responsbility pattern for logging?
# We can have a Regular python logger -> Rich Formatted Logger -> Log to File!?
# Note: The default python logging.getLogger() is a singleton...
# StreamHandler, FileHandler (log to disk)
# Handlers send the log records (created by loggers) to the appropriate destination.


class App:
    """
    App configuration Singleton.
    This isn't an anti-pattern because it's read only data.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            _instance = super().__new__(cls)
        return cls._instance

    # TODO: Take toml config file path?
    def __init__(self, config_file_path: str, logger: Optional[logging.Logger] = None):
        self.__config = utils.load_toml_file(config_file_path)
        self.__args = get_cmd_args()

    def log(self, msg: str, level: int) -> None:
        self.__logger.log(msg, level)

    def run(self):
        args = get_cmd_args()
        stack_exchange = None

        if self.__config.redis_host and self.__config.redis_port and self.__config.redis_password:
            redis_cache = RedisCache(
                host=self.__config.redis_host, port=self.__config.redis_port, password=self.__config.redis_password
            )

            stack_exchange = CachedStackExchange(stack_exchange_service=StackExchange(), cache=redis_cache)
        else:
            stack_exchange = StackExchange()

        query = args.query

        search_results = stack_exchange.search(query)
        print(search_results)
