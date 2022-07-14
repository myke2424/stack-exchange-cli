from dataclasses import dataclass


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

        def with_filter(self, filter: str):
            """
            Filter used on the request to modify the response
            read more here: https://api.stackexchange.com/docs/filters
            """
            self.__filter = filter
            return self

        def with_tags(self, tags: str):
            """
            A list of tags which at least one will be present on all returned questions.
            :param tags: Space seperated tags, i.e. "python c++ rust"
            """
            self.__tags = ";".join(tags.split(" "))
            return self

        def accepted_only(self):
            """Return only questions with accepted answers"""
            self.__accepted = True
            return self

        def n_results(self, n: int):
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
        item_dict = {}

        # match response fields with class attributes
        for k, v in response_item.items():
            if k in attrs:
                item_dict[k] = v

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
    def from_json(cls, json_) -> "SearchResult":
        """Deserialize JSON to SearchResult obj"""
        question, answer = Question(**json_["question"]), Answer(**json_["answer"])
        return cls(question, answer)

    def to_json(self) -> dict:
        """Serialize to JSON"""
        return {"question": self.question.__dict__, "answer": self.answer.__dict__}
