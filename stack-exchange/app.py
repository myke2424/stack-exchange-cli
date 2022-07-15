import argparse
import logging

from .cache import RedisCache
from .commands import get_cmd_args
from .models import Config
from .search import CachedStackExchange, Searchable, StackExchange


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs) -> "Singleton":
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class App(Singleton):
    """
    App singleton contains all the read-only state data that must be accessible across the application.
    Configuration data includes - (redis, api, logging, cmd line arguments)
    """

    _CONFIG_FILE_PATH = "config.yaml"

    def __init__(self) -> None:
        self.__config = Config.from_yaml_file(self._CONFIG_FILE_PATH)
        self.__args = get_cmd_args()
        self.__logger = logging.getLogger(__name__)
        self._configure_logger()

    @property
    def config(self) -> Config:
        return self.__config

    @property
    def args(self) -> argparse.ArgumentParser:
        return self.__args

    def _configure_logger(self) -> None:
        log_level = self.config.logging.log_level
        handlers = [logging.StreamHandler()]

        if self.config.logging.log_to_file:
            handlers.append(logging.FileHandler(self.config.logging.log_filename))

        logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)

    def get_stack_exchange_service(self) -> Searchable:
        """
        Get stack exchange object used for searching.
        If redis configuration is set in config.yaml, cache search requests with proxy object.
        """
        stack_exchange = StackExchange(self.config.api.version)
        if self.config.redis.host and self.config.redis.port and self.config.redis.password:
            redis_db = RedisCache(**self.config.redis.__dict__)
            return CachedStackExchange(cache=redis_db, stack_exchange_service=stack_exchange)
        return stack_exchange
