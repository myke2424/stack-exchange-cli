from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Question:
    title: str
    body: str
    url: str
    score: int
    accepted_answer_id: int
    creation_date: str

    @classmethod
    def from_search_response_item(cls, search_response: dict) -> "Question":
        return cls(
            title=search_response["title"],
            body=search_response["body"],
            url=search_response["link"],
            score=search_response["score"],
            accepted_answer_id=search_response["accepted_answer_id"],
            creation_date=search_response["creation_date"],
        )


@dataclass(frozen=True)
class Answer:
    body: str
    score: int
    creation_date: str

    @classmethod
    def from_answer_response_item(cls, answer_response: dict) -> "Answer":
        return cls(
            body=answer_response["body"],
            score=answer_response["score"],
            creation_date=answer_response["creation_date"],
        )


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
