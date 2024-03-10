import dataclasses


@dataclasses.dataclass(frozen=True)
class Team:
    team_id: int
    team_name: str
    NOC: str
