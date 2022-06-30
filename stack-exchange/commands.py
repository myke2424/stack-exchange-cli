import argparse
from abc import ABC
from typing import List


class Command(ABC):
    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        """Add command to parser"""


class QueryCommand(Command):
    """
    Search query used to search a stack exchange website
    """

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-q", "--query", nargs="+", help=self.__doc__, required=True)


class SiteCommand(Command):
    """Stack exchange website used to search the query on - default=stackoverflow"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-s", "--site", help=self.__doc__, default="stackoverflow")


class TagsCommand(Command):
    """Tags used in stackexchange search"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("-t", "--tags", help=self.__doc__, required=False, default=[], type=list)


class InteractiveCommand(Command):
    """Interactive search flag, used to display search results and allow user to interactive with them"""

    def prepare_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "-i",
            "--interactive",
            help=self.__doc__,
            required=False,
            default=False,
            type=bool,
        )


_COMMANDS: List[Command] = [
    QueryCommand(),
    SiteCommand(),
    TagsCommand(),
    InteractiveCommand(),
]


def get_cmd_args() -> argparse.ArgumentParser:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="StackExchange Command Line Search Client")

    for command in _COMMANDS:
        assert command.__class__.__name__.endswith("Command")
        command.prepare_parser(parser)

    args = parser.parse_args()
    return args
