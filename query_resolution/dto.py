from dataclasses import dataclass


@dataclass(frozen=True)
class AdlTakesStatement:
    action: str
    time: int


@dataclass(frozen=True)
class Fluent:
    name: str
    negated: bool


@dataclass(frozen=True)
class AdlCausesStatement:
    action: str
    fluent: Fluent
    condition_fluents: list[Fluent]


@dataclass(frozen=True)
class ObservationStatement:
    fluent: Fluent
    time: int


@dataclass(frozen=True)
class ActionStatement:
    action: str
    time: int
