import argparse
import logging

from .commands import get_cmd_args
from .models import Config


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
