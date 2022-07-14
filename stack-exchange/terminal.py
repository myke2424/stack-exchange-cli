""" Terminal UI """

import logging

from rich import print as rprint
from rich.console import Console
from . import utils
import sys
from .models import SearchResult
import logging
import webbrowser

logger = logging.getLogger(__name__)


class Terminal:
    """Responsible for handling user input and displaying results to the terminal"""

    def __init__(self, interactive_search: bool) -> None:
        self.__console = Console()
        self.__interactive_search = interactive_search

    def display(self, query: str, search_results: list[SearchResult]) -> None:
        """Main interface to display terminal output and interaction"""
        if not self.__interactive_search:
            logger.info("Using fast-search...")
            self._print_result(search_results[0])
            sys.exit(0)

        self._interactive_search_handler(query, search_results)

    def _interactive_search_handler(self, query: str, search_results: list[SearchResult]):
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
            command = input("")

            match command:
                case "o":
                    webbrowser.open(search_result.question.link)
                    continue
                case "g":
                    break
                case "q":
                    sys.exit(0)
                case other:
                    print("Invalid Command!")

    @staticmethod
    def _print_result_titles(query: str, search_results: list[SearchResult]) -> None:
        """Print all the question titles from search results to the console"""
        rprint(f"\n[bold green]Search results for query: '{''.join(query)}'\n")
        for idx, result in enumerate(search_results):
            rprint(f"{idx + 1}. [bold magenta]{result.question.title}")
        print("\n")

    def _print_result(self, search_result: SearchResult) -> None:
        """Pretty print a search result to the console using Rich Formatting"""
        rprint(f"\n[bold red]Question: [bold green]{search_result.question.title} \n")
        self.__console.print(utils.html_to_markdown(search_result.question.body))

        rprint(f"\n[bold red]Top Answer: [bold red] \n")
        self.__console.print(utils.html_to_markdown(search_result.answer.body))
        print("\n")
