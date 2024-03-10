import dataclasses


@dataclasses.dataclass(frozen=True)
class Sport:
    sport_id: int
    name: str
