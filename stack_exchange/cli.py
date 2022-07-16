""" Terminal UI """

import logging
import os
import sys
import webbrowser
from enum import Enum

from rich import print as rprint
from rich.console import Console

from . import utils
from .models import Answer, Question, SearchResult

logger = logging.getLogger(__name__)


class UserCommand(Enum):
    OPEN_BROWSER = "o"
    GO_BACK = "g"
    QUIT = "q"


class Terminal:
    """Responsible for handling user input and displaying results to the terminal"""

    def __init__(self, interactive_search: bool) -> None:
        self.__console = Console()
        self.__interactive_search = interactive_search
        self.__terminal_size = os.get_terminal_size()

    def display(self, query: str, search_results: list[SearchResult]) -> None:
        """Main interface to display terminal output and interaction"""
        if not self.__interactive_search:
            logger.info("Using fast-search...")
            self._print_result(search_results[0])
            sys.exit(0)

        self._interactive_search_handler(query, search_results)

    def _interactive_search_handler(self, query: str, search_results: list[SearchResult]) -> None:
        """Handle user input and display results to console for interactive mode"""
        while True:
            self._print_result_titles(query, search_results)
            selected_result_idx = self._prompt_question_number_input(search_results)
            search_result = search_results[selected_result_idx]
            self._print_result(search_result)

            rprint(
                f"\n[bold green]Enter [bold red]'q'[/bold red] to quit |  [bold red]'g'[/bold red] to go back to "
                f"results | [bold red]'o'[/bold red] to open question in browser "
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
            except ValueError:
                rprint("[bold red]INVALID INPUT... please enter a valid question number")
        return selected_result_idx

    @staticmethod
    def _command_input_handler(search_result: SearchResult) -> None:
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
                    case UserCommand.QUIT:
                        sys.exit(0)
            except ValueError:
                print(f"'{command}'is an invalid command!")

    @staticmethod
    def _print_result_titles(query: str, search_results: list[SearchResult]) -> None:
        """Print all the question titles from search results to the console"""
        rprint(f"\n[bold green]Search results for query:[/bold green] [red]'{''.join(query)}'\n")
        for idx, result in enumerate(search_results):
            rprint(f"{idx + 1}. [bold magenta]{result.question.title}")
        print("\n")

    def _print_question(self, question: Question) -> None:
        rprint("[bold green]-" * self.__terminal_size.columns)
        self.__console.print(utils.html_to_markdown("<h1>Question</h1>"), style="green")
        rprint(f"\n[bold red][bold green]{question.title} \n")
        self.__console.print(utils.html_to_markdown(question.body))
        rprint("[bold green]-" * self.__terminal_size.columns)

    def _print_answer(self, answer: Answer) -> None:
        rprint("[bold blue]-" * self.__terminal_size.columns)
        self.__console.print(utils.html_to_markdown("<h1> Answer </h1>"), style="blue")
        print("\n")
        self.__console.print(utils.html_to_markdown(answer.body))
        rprint("[bold blue]-" * self.__terminal_size.columns)

    def _print_result(self, search_result: SearchResult) -> None:
        """Pretty print a search result to the console using Rich Formatting"""
        self._print_question(search_result.question)
        self._print_answer(search_result.answer)
        rprint(f"[bold green]Question link:[/bold green] {search_result.question.link}")
