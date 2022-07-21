"""
Main file to run the application

TO RUN THE APPLICATION, DO NOT RUN THIS FILE DIRECTLY, IT WILL NOT WORK DUE TO RELATIVE PACKAGE IMPORTS!

Instead, run the following command in the root directory: python3.10 -m stack_exchange <commands>
"""

import sys

from rich import print as rprint

from .app import App
from .cli import Terminal
from .search import SearchRequest


def main():
    """Main function to run the application"""
    app = App()
    terminal = Terminal(interactive_search=app.args.interactive, jsonify=app.args.json)

    # Client passed in command line arg '-a' to view the alias from cache - display it to the client and exit
    if app.args.alias:
        terminal.print_alias()
        sys.exit(0)

    if app.args.query is None:
        print("Search requires a query string - please use the '-q' or '--query' argument")
        sys.exit(1)

    stack_exchange = app.get_stack_exchange_service()

    # If the client doesn't use a -s cmd flag to specify the site, use the default site in config.yaml
    site = app.args.site or app.config.api.default_site

    search_request = (
        SearchRequest.Builder(app.args.query, site)
            .with_tags(app.args.tags)
            .accepted_only()
            .n_results(app.args.num)
            .sort_by(app.args.sortby)
            .build()
    )

    search_results = stack_exchange.search(search_request)
    terminal.display(app.args.query, search_results)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        rprint("[bold red]Search Failed")
        rprint(f"[bold red]Error Reason:[/bold red] - {e}")
        sys.exit(1)
