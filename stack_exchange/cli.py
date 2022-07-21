"""
Module contains the application code that displays the UI to the client via the terminal.
It's also responsible for handling any user input.
"""

import json
import logging
import os
import sys
import webbrowser
from enum import Enum

from rich import print as rprint
from rich.console import Console

from . import utils
from .app import App
from .errors import InvalidConfigurationError
from .models import Answer, Question, SearchResult

logger = logging.getLogger(__name__)


class UserCommand(Enum):
    """Enum to represent user input commands in interactive search mode"""

    OPEN_BROWSER = "o"
    GO_BACK = "g"
    QUIT = "q"
    SAVE_TO_CACHE = "s"


class Terminal:
    """Responsible for handling user input and displaying results to the terminal"""

    def __init__(self, interactive_search: bool, jsonify: bool = False) -> None:
        self.__console = Console()
        self.__interactive_search = interactive_search
        self.__terminal_size = self._get_terminal_size()
        self.__jsonify = jsonify

    def display(self, query: str, search_results: list[SearchResult]) -> None:
        """Main interface to display terminal output and interaction"""
        if not self.__interactive_search:
            logger.info("Using fast-search...")

            # Client uses the -j or --json cmd flag to dump search-results to stdout as json
            if self.__jsonify:
                print(json.dumps([sr.to_json() for sr in search_results], indent=2))
            else:
                self._print_result(search_results[0])
            sys.exit(0)

        self._interactive_search_handler(query, search_results)

    def print_alias(self) -> None:
        """Display cached search result to the console under the given alias passed in by cmd line argument '-a'"""
        app = App()
        alias = app.args.alias

        rprint(f"\nFetching alias='{alias}' from cache")

        if app.redis_db is None:
            raise InvalidConfigurationError("Redis not configured in config.yaml... Failed to view alias in cache")

        cached_search_result = app.redis_db.get(alias)

        if cached_search_result is None:
            rprint(f"[bold red]Alias: '{alias}' doesn't exist in cache... exiting")
            sys.exit(1)

        logger.info(f"Printing alias: {alias} - cached search results to console")
        self._print_result(SearchResult.from_json(cached_search_result))

    @staticmethod
    def flush_cache_prompt() -> None:
        """Prompt the user to flush the cache"""
        while True:
            try:
                should_flush = input("Are you sure you want to flush the cache? Type 'y' for YES | 'n' for NO ")
                if should_flush != "n" and should_flush != "y":
                    raise ValueError
                else:
                    break
            except ValueError:
                rprint("[bold red]Please enter a valid value: 'y' or 'n'")

        if should_flush == "y":
            if App().redis_db is None:
                raise InvalidConfigurationError("Redis not configured in config.yaml... Failed to flush cache")
            App().redis_db.clear()
            rprint("[bold green]Cache has been flushed!")

    def _get_terminal_size(self) -> int:
        """Used to get size of terminal"""
        try:
            terminal_size = os.get_terminal_size()
            return terminal_size.columns
            # some IDEs (PyCharm) will raise this exception when getting terminal size
        except OSError:
            logger.debug("Using default terminal size...")
            return 75

    def _interactive_search_handler(self, query: str, search_results: list[SearchResult]) -> None:
        """Handle user input and display results to console for interactive mode"""
        while True:
            self._print_result_titles(query, search_results)
            selected_result_idx = self._prompt_question_number_input(search_results)
            search_result = search_results[selected_result_idx]
            self._print_result(search_result)

            rprint(
                f"\n[bold green]Enter [bold magenta]'q'[/bold magenta] to quit |  [bold magenta]'g'[/bold magenta] to go back to "
                f"results | [bold magenta]'o'[/bold magenta] to open question in browser | [bold magenta]'s'[/bold magenta] Save to cache under an alias "
            )

            self._command_input_handler(search_result)

    @staticmethod
    def _prompt_question_number_input(search_results: list[SearchResult]) -> int:
        """Prompt user for the selected question #, to be used as an index into search results"""
        while True:
            try:
                selected_result_idx = int(input("Enter question number to view answer: ")) - 1

                if 0 <= selected_result_idx <= len(search_results) - 1:
                    break
                else:
                    raise ValueError
            except ValueError:
                rprint("[bold red]INVALID INPUT... please enter a valid question number")
        return selected_result_idx

    @staticmethod
    def _prompt_save_to_cache_alias(search_result: SearchResult) -> None:
        """Prompt the user for the alias used to save the search result in the cache, used in interactive mode"""
        alias = input("Enter in an alias for the search result to save to the cache: ")
        logger.debug(f"Setting alias={alias} for search result {search_result}")

        if App().redis_db is None:
            raise InvalidConfigurationError("Redis not configured in config.yaml... Failed to save alias to cache")

        App().redis_db.set(alias, search_result.to_json())
        rprint(f"[bold green]Saved search result under alias: {alias}")

    def _command_input_handler(self, search_result: SearchResult) -> None:
        """Prompt user input for a command in interactive mode and handle the input"""
        while True:
            try:
                command = input("")

                match UserCommand(command):
                    case UserCommand.OPEN_BROWSER:
                        webbrowser.open(search_result.question.link)
                        continue
                    case UserCommand.GO_BACK:
                        break
                    case UserCommand.SAVE_TO_CACHE:
                        self._prompt_save_to_cache_alias(search_result)
                    case UserCommand.QUIT:
                        sys.exit(0)
            except ValueError:
                print(f"'{command}'is an invalid command!")

    @staticmethod
    def _print_result_titles(query: str, search_results: list[SearchResult]) -> None:
        """Print all the question titles from search results to the console"""
        rprint(f"\n[bold green]Search results for query:[/bold green] [bold magenta]'{''.join(query)}'\n")
        for idx, result in enumerate(search_results):
            date = utils.epoch_time_to_datetime_str(result.question.creation_date)
            rprint(
                f"{idx + 1}. [bold magenta]{result.question.title}[/bold magenta][bold green] [{date} | {result.question.score} votes]"
            )
        print("\n")

    def _print_question(self, question: Question) -> None:
        """Print the search result question to the terminal using rich formatting"""
        rprint("[bold green]-" * self.__terminal_size)
        date = utils.epoch_time_to_datetime_str(question.creation_date)
        self.__console.print(
            utils.html_to_markdown(f"<h1>Question | {date} | {question.score} votes</h1>"), style="green"
        )
        rprint(f"\n[bold red][bold green]{question.title} \n")
        self.__console.print(utils.html_to_markdown(question.body))
        rprint("[bold green]-" * self.__terminal_size)

    def _print_answer(self, answer: Answer) -> None:
        """Print the search result answer to the format using rich formatting"""
        rprint("[bold blue]-" * self.__terminal_size)
        date = utils.epoch_time_to_datetime_str(answer.creation_date)
        self.__console.print(utils.html_to_markdown(f"<h1>Answer | {date} | {answer.score} votes</h1>"), style="blue")
        print("\n")
        self.__console.print(utils.html_to_markdown(answer.body))
        rprint("[bold blue]-" * self.__terminal_size)

    def _print_result(self, search_result: SearchResult) -> None:
        """Pretty print a search result to the console using Rich Formatting"""
        self._print_question(search_result.question)
        self._print_answer(search_result.answer)
        rprint(f"[bold green]Question link:[/bold green] {search_result.question.link}\n")
