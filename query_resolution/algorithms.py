import random

from query_resolution.dto import (
    ActionStatement,
    AdlCausesStatement,
    AdlTakesStatement,
    Fluent,
    ObservationStatement,
)


def resolve_realizable_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    time_bound: int,
) -> bool:
    print(f"{adl_takes_statements=}")
    print(f"{adl_causes_statements=}")
    print(f"{observation_statements=}")
    print(f"{actions_input=}")
    print(f"{time_bound=}")
    return random.random() <= 0.5


def resolve_condition_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    fluents_list: list[Fluent],
    timepoint: int,
    time_bound: int,
):
    print(f"{adl_takes_statements=}")
    print(f"{adl_causes_statements=}")
    print(f"{observation_statements=}")
    print(f"{actions_input=}")
    print(f"{fluents_list=}")
    print(f"{timepoint=}")
    print(f"{time_bound=}")
    return random.random() <= 0.5
