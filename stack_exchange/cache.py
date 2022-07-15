import json
import logging
from abc import ABC, abstractmethod
from typing import Any

import redis

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


class RedisCache(Cache):
    def __init__(self, host: str, port: int, password: str) -> None:
        self.__db = redis.Redis(host=host, port=port, password=password)
        self._validate_connection()

    def _validate_connection(self) -> None:
        """Validate connection to Redis DB is working"""
        if not self.__db.ping():
            raise RedisConnectionError("Failed to connect to Redis Database...")

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
