import sys

from .app import App
from .cli import Terminal
from .search import SearchRequest


def main():
    """Main function to run the application"""
    app = App()
    stack_exchange = app.get_stack_exchange_service()

    search_request = (
        SearchRequest.Builder(app.args.query, app.args.site)
        .with_tags(app.args.tags)
        .accepted_only()
        .n_results(app.args.num)
        .build()
    )

    search_results = stack_exchange.search(search_request)

    terminal = Terminal(interactive_search=app.args.interactive)
    terminal.display(app.args.query, search_results)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Search Failed")
        print(f"Error: {e}")
        sys.exit(1)
