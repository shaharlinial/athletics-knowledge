import dataclasses


@dataclasses.dataclass(frozen=True)
class Question:
    text: str
    answers: list
    correct_answer: str
