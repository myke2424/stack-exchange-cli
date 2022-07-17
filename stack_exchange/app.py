import argparse
import logging
import os

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

    The use of the Singleton in this instance is justified because the data contained is only read-only data,
    and all configuration data is immutable. Therefore, there is no risk of hard-to-trace bugs due to
    global state modification.
    """

    def __init__(self) -> None:
        self.__args = get_cmd_args()
        self.__config_file_path = self.__args.config or os.path.join(os.path.dirname(__file__), "../config.yaml")
        self.__config = Config.from_yaml_file(self.__config_file_path)
        self.__logger = logging.getLogger(__name__)
        self._setup()

    def _setup(self) -> None:
        self._configure_logger()
        self.__logger.debug(f"Command Arguments: {self.__args}")
        self.__logger.debug(f"Using config file: {self.__config_file_path}")
        self.__logger.debug(self.__config)

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

        if self.args.verbose:
            log_level = logging.DEBUG

        logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)

    def get_stack_exchange_service(self) -> Searchable:
        """
        Get stack exchange object used for searching.
        If redis configuration is set in config.yaml, cache search requests with proxy object.
        """
        stack_exchange = StackExchange(self.config.api)
        if self.config.redis.host and self.config.redis.port and self.config.redis.password:
            self.__logger.info("Using cached stack exchange service")
            redis_db = RedisCache(**self.config.redis.__dict__)
            return CachedStackExchange(cache=redis_db, stack_exchange_service=stack_exchange)
        return stack_exchange
