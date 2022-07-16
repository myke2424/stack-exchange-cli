""" Module that handles command line argument parsing """

import argparse
from abc import ABC


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
        parser.add_argument("-n", "--num", help=self.__doc__, default=30, required=False)


class VerboseLoggingCommand(Command):
    """Verbose logging flag"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-v", "--verbose", help=self.__doc__, action="store_true", required=False)


_COMMANDS: list[Command] = [
    QueryCommand(),
    SiteCommand(),
    TagsCommand(),
    InteractiveCommand(),
    NumCommand(),
    VerboseLoggingCommand(),
]


def get_cmd_args() -> argparse.ArgumentParser:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Stack Exchange Command Line Search Client")

    for command in _COMMANDS:
        assert isinstance(command, Command)
        command.prepare_parser(parser)

    args = parser.parse_args()
    return args
