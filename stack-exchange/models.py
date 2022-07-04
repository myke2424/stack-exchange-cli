from dataclasses import dataclass
from typing import List, Optional


# TODO: Not sure if I want to use inheritance here.
@dataclass(frozen=True)
class SearchResultItem:
    body: str
    score: int
    creation_date: str

    @classmethod
    def from_response_item(cls, search_response: dict) -> "SearchResultItem":
        attrs = cls.__dataclass_fields__.keys()
        item_dict = {}

        for k, v in search_response.items():
            if k in attrs:
                item_dict[k] = v

        if len(item_dict) != len(attrs):
            raise ValueError("Search response doesn't contain all required fields")
        return cls(**item_dict)


@dataclass(frozen=True)
class Question(SearchResultItem):
    title: str
    link: str
    accepted_answer_id: int


@dataclass(frozen=True)
class Answer(SearchResultItem):
    is_accepted: bool


# TODO: Not sure if I need this.
@dataclass(frozen=True)
class Comment(SearchResultItem):
    pass


# TODO: Potentially add comment to result
@dataclass(frozen=True)
class SearchResult:
    question: Question
    answer: Answer

    @classmethod
    def from_json(cls, json_) -> "SearchResult":
        question, answer = Question(**json_["question"]), Answer(**json_["answer"])
        return cls(question, answer)

    def to_json(self) -> dict:
        return {"question": self.question.__dict__, "answer": self.answer.__dict__}


# TODO: Remove, since we replaced with dictionary
@dataclass(frozen=True)
class SearchParams:
    query: str
    count: int
    tags: Optional[List[str]]
    site: str
    in_body: bool

    def to_json(self) -> dict:
        """Build parameter dictionary for search requests"""
        json_ = {
            "q": self.query,
            "site": self.site,
            "accepted": True,
            "sort": "votes",
            "filter": "withbody",
            "sort": "votes",
        }

        if self.in_body:
            json_["body"] = self.query
            del json_["q"]  # remove query since we're searching by body

        if self.tags is not None:
            json_["tagged"] = ";".join(self.tags)

        return json_
