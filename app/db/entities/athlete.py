import dataclasses


@dataclasses.dataclass(frozen=True)
class Athlete:
    athlete_id: int
    name: str
    sex: str
