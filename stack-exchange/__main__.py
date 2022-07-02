import logging

from . import commands, utils
from .cache import RedisCache
from .search import CachedStackExchange, StackExchange

config_file_path = "config.toml"
config = utils.load_toml_file(config_file_path)

log_level = config["logging"]["level"]
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


def main():
    stack_exchange = StackExchange()

    # Create cached search client if redis config
    # Load config file into immutable dataclass might be better after all...
    if config["redis"]["host"] and config["redis"]["port"] and config["redis"]["password"]:
        redis_cache = RedisCache(**config["redis"])
        stack_exchange = CachedStackExchange(stack_exchange_service=StackExchange(), cache=redis_cache)

    args = commands.get_cmd_args()
    logger.debug(f"Command line arguments: {args}")
    search_results = stack_exchange.search(query=args.query, site=args.site)
    print(search_results)


if __name__ == "__main__":
    main()
