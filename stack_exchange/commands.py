""" Module that handles command line argument parsing """

import argparse
from abc import ABC

from ._version import __version__


class Command(ABC):
    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        """Add command to parser"""


class QueryCommand(Command):
    """Search query used to search a stack exchange website [REQUIRED]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-q", "--query", nargs="+", help=self.__doc__, required=True)


class SiteCommand(Command):
    """Stack exchange website used to search the query on [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-s", "--site", help=self.__doc__)


class TagsCommand(Command):
    """Space seperated tags used in stackexchange search [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-t", "--tags", help=self.__doc__, required=False, default="")


class InteractiveCommand(Command):
    """Interactive search flag, used to display search results and allow user to interact with them [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-i",
            "--interactive",
            help=self.__doc__,
            required=False,
            action="store_true",
        )


class NumCommand(Command):
    """Number of results to display when interactive searching [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-n", "--num", help=self.__doc__, default=30, type=int, required=False)


class SortByCommand(Command):
    """Sort the search results by the following method types [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-sb",
            "--sortby",
            help=self.__doc__,
            choices=["votes", "creation", "relevance", "activity"],
            default="votes",
            required=False,
        )


class ApiKeyCommand(Command):
    """Pass in a stack exchange API key manually instead of using a config file to avoid request throttling [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-k",
            "--key",
            help=self.__doc__,
            required=False,
        )


class SetApiKeyCommand(Command):
    """Set stack exchange API key in config.yaml, to avoid repeating using -k search commands [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-sk",
            "--set-key",
            help=self.__doc__,
            required=False,
        )


class ConfigFileCommand(Command):
    """Pass in a config.yaml file path to use for api, redis and logging settings [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-c",
            "--config",
            help=self.__doc__,
            required=False,
        )


class VerboseLoggingCommand(Command):
    """Verbose logging flag [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-vv", "--verbose", help=self.__doc__, action="store_true", required=False)


class VersionCommand(Command):
    """Application version [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-v", "--version", help=self.__doc__, action="version", version=__version__)


class FlushCacheCommand(Command):
    """Flush all keys/values in redis cache, used for testing [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-fc", "--flush-cache", help=self.__doc__, action="store_true")


class OverwriteCacheCommand(Command):
    """Overwrite cache value if key exists in cache [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-oc", "--overwrite-cache", help=self.__doc__, action="store_true")


class JsonCommand(Command):
    """Print search results as json to stdout [OPTIONAL]"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-j", "--json", help=self.__doc__, action="store_true")


class GoogleSearch(Command):
    """Use google search instead of stack-exchange API for searching"""

    # TODO: Implement functionality


_COMMANDS: list[Command] = [
    QueryCommand(),
    SiteCommand(),
    TagsCommand(),
    InteractiveCommand(),
    NumCommand(),
    SortByCommand(),
    ApiKeyCommand(),
    ConfigFileCommand(),
    VerboseLoggingCommand(),
    VersionCommand(),
    OverwriteCacheCommand(),
    FlushCacheCommand(),
    JsonCommand(),
    SetApiKeyCommand()
]


def get_cmd_args() -> argparse.ArgumentParser:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Stack Exchange Command Line Search Client - search stack exchange websites in your terminal!",
        epilog='Have fun searching!'
    )

    for command in _COMMANDS:
        assert isinstance(command, Command)
        command.prepare_parser(parser)

    args = parser.parse_args()
    return args
