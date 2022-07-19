import sys

from rich import print as rprint

from .app import App
from .cli import Terminal
from .search import SearchRequest


def main():
    """Main function to run the application"""
    app = App()
    stack_exchange = app.get_stack_exchange_service()
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

    terminal = Terminal(interactive_search=app.args.interactive, jsonify=app.args.json)
    terminal.display(app.args.query, search_results)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        rprint("[bold red]Search Failed")
        rprint(f"[bold red]Error Reason:[/bold red] - {e}")
        sys.exit(1)
