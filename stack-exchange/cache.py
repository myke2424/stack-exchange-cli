import redis
import json
from abc import ABC, abstractmethod


class Cache(ABC):
    @abstractmethod
    def get(self, key):
        """ Get value with associated key in cache """
        pass

    @abstractmethod
    def set(self, key, value):
        """ Set key with associated value in cache """
        pass


class RedisCache(Cache):
    def __init__(self, host: str, port: int, password: str):
        self.__db = redis.Redis(host=host, port=port, password=password)

    def get(self, key):
        value = self.__db.get(key).decode('utf-8')
        # try deserializing value in the case its json encoded
        try:
            value = json.loads(value)
        except (ValueError, TypeError):
            pass
        return value

    def set(self, key, value) -> None:
        # if value is json, serialize it to a json string
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.__db.set(key, value)
