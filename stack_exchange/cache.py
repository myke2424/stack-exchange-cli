import json
import logging
from abc import ABC, abstractmethod
from typing import Any

import redis
from rich import print as rprint

from .errors import RedisConnectionError

logger = logging.getLogger(__name__)


class Cache(ABC):
    """
    An interface for a cache keyed by a string with any data type as the value.

    Derived classes can implement their own data serialization/deserialization.
    """

    @abstractmethod
    def get(self, key: str) -> Any:
        """Get value with associated key in cache"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Set key with associated value in cache"""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all keys/values in cache"""
        pass


class RedisCache(Cache):
    def __init__(self, host: str, port: int, password: str, flush: bool = False) -> None:
        self.__db = redis.Redis(host=host, port=port, password=password)
        self._flush = flush
        self._setup()

    def _setup(self) -> None:
        self._validate_connection()

        if self._flush:
            self._flush_prompt()

    def _validate_connection(self) -> None:
        if not self.__db.ping():
            raise RedisConnectionError("Failed to connect to Redis Database...")

    def _flush_prompt(self) -> None:
        while True:
            try:
                should_flush = input("Are you sure you want to flush the cache? Type 'y' for YES | 'n' for NO ")
                print(should_flush)
                if should_flush != "n" and should_flush != "y":
                    raise ValueError
                else:
                    break
            except ValueError:
                rprint("[bold red]Please enter a valid value: 'y' or 'n'")

        if should_flush == "y":
            self.clear()

    def get(self, key: str) -> Any:
        logger.debug(f"Reading cache - key: {key}")
        value = self.__db.get(key)

        if value is not None and isinstance(value, bytes):
            value = value.decode("utf-8")

        # try deserializing value in the case its json encoded
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            pass
        return value

    def set(self, key: str, value: Any) -> None:
        # if value is json, serialize it to a json string
        logger.debug(f"Writing to cache - key: {key}")
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.__db.set(key, value)

    def clear(self) -> None:
        logger.debug("FLUSHING REDIS DATABASE!!!")
        self.__db.flushdb()
