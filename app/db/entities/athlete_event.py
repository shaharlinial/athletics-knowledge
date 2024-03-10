import dataclasses


@dataclasses.dataclass(frozen=True)
class AthleteEvent:
    athlete_id: int
    team_id: int
    event_id: int
    medal: str
    weight: int
    height: int
    age: int
