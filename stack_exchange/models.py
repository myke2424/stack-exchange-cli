from dataclasses import dataclass

from . import utils


@dataclass
class SearchRequest:
    """
    Model representation of a search GET request to the stack exchange
    /search/advanced API endpoint (https://api.stackexchange.com/docs/advanced-search).
    """

    query: str
    tags: str
    num: int
    site: str
    accepted: str
    filter: str

    def to_json(self) -> dict:
        """JSON representation of search request"""
        json_ = {
            "q": self.query,
            "site": self.site,
            "accepted": self.accepted,
            "tags": self.tags,
            "filter": self.filter,
            "sort": "votes",
        }

        return json_

    class Builder:
        """
        Builder Design Pattern is used here to construct a search request object for the Stack Exchange API.
        This may feel like unidiomatic python, as keyword arguments and optional arguments can potentially replace
        'simple' versions of a builder pattern. However, a search request can get quite complex, as the API supports
        over 20 parameters (not all currently supported).

        Instead of forcing the caller to use keyword arguments and a complicated constructor,
        we can use the builder pattern to create a fluent API for building the request.
        """

        def __init__(self, query: str, site: str) -> None:
            """
            :param query: Search query string
            :param site: Stack Exchange website to search on
            """
            self.__query = query
            self.__site = site
            self.__tags = None
            self.__num = None
            self.__accepted = None
            self.__filter = "withbody"

        def with_filter(self, filter: str) -> "Builder":
            """
            Filter used on the request to modify the response
            read more here: https://api.stackexchange.com/docs/filters
            """
            self.__filter = filter
            return self

        def with_tags(self, tags: str) -> "Builder":
            """
            A list of tags which at least one will be present on all returned questions.
            :param tags: Space seperated tags, i.e. "python c++ rust"
            """
            self.__tags = ";".join(tags.split(" "))
            return self

        def accepted_only(self) -> "Builder":
            """Return only questions with accepted answers"""
            self.__accepted = True
            return self

        def n_results(self, n: int) -> "Builder":
            """Number of search results we want"""
            self.__num = n
            return self

        def build(self) -> "SearchRequest":
            """Build the SearchRequest object"""
            request = {
                "query": self.__query,
                "tags": self.__tags,
                "num": self.__num,
                "site": self.__site,
                "accepted": self.__accepted,
                "filter": self.__filter,
            }

            return SearchRequest(**request)


@dataclass(frozen=True)
class StackResponseItem:
    """
    Model representation of a StackExchange Response Item
    Base class with common fields stack exchange entities can inherit, i.e. question, answer, comment */
    """

    body: str
    score: int
    creation_date: str

    @classmethod
    def from_response_item(cls, response_item: dict) -> "StackResponseItem":
        """Alternate constructor to create the object based on the raw GET response from the stack exchange API"""
        attrs = cls.__dataclass_fields__.keys()

        # match response fields with class attributes
        item_dict = {k: v for k, v in response_item.items() if k in attrs}

        if len(item_dict) != len(attrs):
            raise ValueError(
                "response_item dict doesn't contain all required fields to construct StackResponseItem obj"
            )
        return cls(**item_dict)


@dataclass(frozen=True)
class Question(StackResponseItem):
    """Model representation of a StackExchange Question"""

    title: str
    link: str
    accepted_answer_id: int


@dataclass(frozen=True)
class Answer(StackResponseItem):
    """Model representation of a StackExchange Answer"""

    is_accepted: bool


@dataclass(frozen=True)
class SearchResult:
    """Model representation of a question and answer on a stack exchange thread"""

    question: Question
    answer: Answer

    @classmethod
    def from_json(cls, json_: dict) -> "SearchResult":
        """Deserialize JSON to SearchResult obj"""
        question, answer = Question(**json_["question"]), Answer(**json_["answer"])
        return cls(question, answer)

    def to_json(self) -> dict:
        """Serialize to JSON"""
        return {"question": self.question.__dict__, "answer": self.answer.__dict__}


@dataclass(frozen=True)
class StackExchangeApiConfig:
    """
    Model representation of the Stack Exchange API Config
    API Configuration is optional, if you don't provide stack exchange API
    credentials, the number of requests will be throttled.

    Read more: (https://api.stackexchange.com/docs/authentication)
    """

    client_id: str
    client_secret: str
    api_key: str
    default_site: str
    version: str


@dataclass(frozen=True)
class RedisConfig:
    """Model representation of a Redis Database configuration - optional if the user wants to cache requests"""

    host: str
    port: int
    password: str


@dataclass(frozen=True)
class LoggingConfig:
    """Model representation of the applications log settings"""

    log_to_file: bool
    log_filename: str
    log_level: str


@dataclass
class Config:
    """Model representation of the application configuration settings"""

    api: StackExchangeApiConfig | None
    redis: RedisConfig | None
    logging: LoggingConfig

    @classmethod
    def from_yaml_file(cls, file_path: str) -> "Config":
        config = utils.load_yaml_file(file_path)
        api, redis, logging = (
            StackExchangeApiConfig(**config["api"]),
            RedisConfig(**config["redis"]),
            LoggingConfig(**config["logging"]),
        )

        return cls(api, redis, logging)
