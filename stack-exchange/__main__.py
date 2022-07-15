from .app import App
from .cache import RedisCache
from .models import Config
from .search import (CachedStackExchange, Searchable, SearchRequest,
                     StackExchange)
from .terminal import Terminal


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
    app = App()
    stack_exchange = get_stack_exchange_service(app.config)

    search_request = (
        SearchRequest.Builder(app.args.query, app.args.site)
        .with_tags(app.args.tags)
        .accepted_only()
        .n_results(20)
        .build()
    )

    search_results = stack_exchange.search(search_request)

    terminal = Terminal(interactive_search=app.args.interactive)
    terminal.display(app.args.query, search_results)


if __name__ == "__main__":
    main()
