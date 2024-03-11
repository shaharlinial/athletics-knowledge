import dataclasses


@dataclasses.dataclass(frozen=True)
class Question:
    text: str
    id: int
    answers: list
    correct_answer: str

