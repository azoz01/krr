from dataclasses import dataclass


@dataclass(frozen=True)
class AdlTakesStatement:
    action: str
    time: int


@dataclass(frozen=True)
class AdlCausesStatement:
    action: str
    fluent: str
    condition_fluents: list[str]


@dataclass(frozen=True)
class ObservationStatement:
    fluent: str
    time: int
    negated: bool


@dataclass(frozen=True)
class ActionStatement:
    action: str
    time: int
