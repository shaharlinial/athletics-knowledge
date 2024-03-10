import dataclasses


@dataclasses.dataclass(frozen=True)
class Country:
    NOC: str
    name: str
