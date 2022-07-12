import logging

from . import commands, utils
from .cache import RedisCache
from .search import CachedStackExchange, StackExchange
from .tui import MyApp

config_file_path = "config.yaml"
config = utils.load_yaml_file(config_file_path)

log_level = config["logging"]["log_level"]
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

"""
Builder Pattern PoC for Building a Search Request


sr = SearchRequestBuilder(site="stackoverflow")
                    .query("Merge two dicts python")
                    .tags("python", "dictionary")
                    .count(5)
                    .accepted() 
                            
This doesn't feel idiomatic...

Maybe Builder Pattern for SearchResult

search_result = SearchResultBuilder()
                        .with_question()
                        .with_accepted_answer()
                        .with_non_accepted_answers()
                        .with_comments()


"""

from rich.markdown import Markdown
from rich.console import Console
from rich.text import Text
from rich import print as p


def main():
    stack_exchange = StackExchange()
    console = Console()
    # Create cached search client if redis config
    # Load config file into immutable dataclass might be better after all...
    if config["redis"]["host"] and config["redis"]["port"] and config["redis"]["password"]:
        redis_cache = RedisCache(**config["redis"])
        stack_exchange = CachedStackExchange(stack_exchange_service=StackExchange(), cache=redis_cache)

    args = commands.get_cmd_args()
    logger.info(f"Command line arguments: {args}")  # TODO: Change to debug, maybe add verbose log flag
    # INTERACTIVE SEARCH START

    # Right now i have to do --i=true, change it so i just do -i and and the flag will be true...
    if args.interactive:
        search_results = stack_exchange.search(query=args.query, site=args.site, num=10)
        p(f"\n[bold green]Search results for query: {''.join(args.query)} \n")
        for idx, result in enumerate(search_results):
            p(f"{idx + 1}.[bold red]{result.question.title}")

        print("\n")
        selected_q = int(input("Enter question number to see answer: "))

        p(f"[bold red]Question: [bold green]{search_results[selected_q - 1].question.title} \n")
        console.print(utils.html_to_markdown(search_results[selected_q - 1].question.body))

        p(f"\n[bold red]Top Answer: [bold red] \n")
        console.print(utils.html_to_markdown(search_results[selected_q - 1].answer.body))

    # INTERACTIVE SEARCH END
    else:
        # FAST SEARCH START
        search_results = stack_exchange.search(query=args.query, site=args.site)

        p(f"[bold red]Question: [bold green]{search_results[0].question.title} \n")
        console.print(utils.html_to_markdown(search_results[0].question.body))

        p(f"[bold red]Top Answer: [bold red] \n")
        console.print(utils.html_to_markdown(search_results[0].answer.body))
        # FAST SEARCH END

        p(f"\n[bold green]Press [SPACE] to see more results, or any other key to exit [bold red] \n")

if __name__ == "__main__":
    main()
