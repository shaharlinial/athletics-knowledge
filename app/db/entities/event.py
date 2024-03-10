import dataclasses


@dataclasses.dataclass(frozen=True)
class Event:
    event_id: int
    olympics_id: int
    event_name: str
    sport: str
