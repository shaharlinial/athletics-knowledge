import dataclasses


@dataclasses.dataclass(frozen=True)
class User:
    id: int
    user_name: str
    first_name: str
    last_name: str
    score: int
