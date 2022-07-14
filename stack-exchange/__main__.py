import argparse
import logging

from . import commands, utils
from .cache import RedisCache
from .search import CachedStackExchange, StackExchange
from .terminal import Terminal
from .search import SearchRequest
from .search import Searchable
from .models import Config, RedisConfig

CONFIG_FILE_PATH = "config.yaml"
N_RESULTS = 20


def get_stack_exchange_service(config: Config) -> Searchable:
    """
    Get stack exchange object used for searching.
    If redis configuration is set in config.yaml, cache search requests with proxy object.
    """
    stack_exchange = StackExchange(config.api.version)
    if config.redis.host and config.redis.port and config.redis.password:
        redis_db = RedisCache(**config.redis.__dict__)
        return CachedStackExchange(cache=redis_db, stack_exchange_service=stack_exchange)
    return stack_exchange


def main():
    """Main function to run the application"""
    args = commands.get_cmd_args()
    config = Config.from_yaml_file(CONFIG_FILE_PATH)
    stack_exchange = get_stack_exchange_service(config)

    search_request = (
        SearchRequest.Builder(args.query, args.site).with_tags(args.tags).accepted_only().n_results(N_RESULTS).build()
    )

    search_results = stack_exchange.search(search_request)

    terminal = Terminal(interactive_search=args.interactive)
    terminal.display(args.query, search_results)


if __name__ == "__main__":
    main()
