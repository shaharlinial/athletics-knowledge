import dataclasses


@dataclasses.dataclass(frozen=True)
class Olympic:
    olympics_id: int
    games: str
    year: str
    season: str
    city: str
