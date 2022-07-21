"""
Module contains the App class which is responsible for storing all application configuration and performing any setup required.
"""

import argparse
import logging
import os
from pathlib import Path

import yaml

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

    The use of the Singleton in this instance is justified because the data contained is only read-only data.
    Therefore, there is no risk of hard-to-trace bugs due to global state modification.
    """

    def __init__(self) -> None:
        self.__args = get_cmd_args()
        _config_file_path = self.__args.config or os.path.join(os.path.dirname(__file__), "../config.yaml")
        self.__config_file_path = Path(_config_file_path)
        self.__config = Config.from_yaml_file(self.__config_file_path.absolute())
        self.__logger = logging.getLogger(__name__)
        self.__redis_db = None
        self._setup()

    def _setup(self) -> None:
        """Run any setup required for the application"""
        self._configure_logger()
        self._configure_redis()

        # use api-key passed in for requests
        if self.__args.key:
            self.__config.api.api_key = self.__args.key

        self.__logger.debug(f"Command Arguments: {self.__args}")
        self.__logger.debug(f"Using config file: {self.__config_file_path}")
        self.__logger.debug(f"Using API Key: {self.__args.key}")
        self.__logger.debug(self.__config)

    def set_api_key(self) -> None:
        """Save api key to config.yaml"""
        with self.__config_file_path.open("r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config["api"]["api_key"] = self.__args.set_key

        with self.__config_file_path.open("w") as f:
            yaml.dump(config, f)

    @property
    def redis_db(self) -> RedisCache:
        """Read-only reference to redis cache"""
        return self.__redis_db

    @property
    def config(self) -> Config:
        """Read-only reference to application config"""
        return self.__config

    @property
    def args(self) -> argparse.ArgumentParser:
        """Read-only reference to command-line arguments"""
        return self.__args

    def _configure_redis(self) -> None:
        """Setup redis database connection if it's configured in config.yaml"""
        if self.config.redis and self.config.redis.host and self.config.redis.port and self.config.redis.password:
            self.__redis_db = RedisCache(**self.config.redis.__dict__)

    def _configure_logger(self) -> None:
        """
        Configure the application logger
        Log configuration can be tweaked via config.yaml (i.e. log to file/log-level)
        """
        log_level = self.config.logging.log_level
        handlers = [logging.StreamHandler()]

        if self.config.logging.log_to_file:
            handlers.append(logging.FileHandler(self.config.logging.log_filename))

        # If the client uses the cmd-line argument '-v', verbose logging will be enabled
        # this will take precedence over the logging configuration set in config.yaml
        if self.args.verbose:
            log_level = logging.DEBUG

        logging.basicConfig(level=log_level, format="%(asctime)s [%(levelname)s] %(message)s", handlers=handlers)

    def get_stack_exchange_service(self) -> Searchable:
        """
        Get the stack exchange object used for searching.
        If redis configuration is set in config.yaml, use the proxy object CachedStackExchange for searching and
        caching search requests.
        """
        stack_exchange = StackExchange(self.config.api)

        if self.redis_db is not None:
            self.__logger.info("Using cached stack exchange service")

            return CachedStackExchange(
                cache=self.redis_db, stack_exchange_service=stack_exchange, overwrite=self.__args.overwrite_cache
            )
        return stack_exchange
