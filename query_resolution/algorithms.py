import random

from query_resolution.dto import (
    ActionStatement,
    AdlCausesStatement,
    AdlTakesStatement,
    ObservationStatement,
    QueryFluent,
)


def resolve_realizable_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
) -> bool:
    print(f"{adl_takes_statements=}")
    print(f"{adl_causes_statements=}")
    print(f"{observation_statements=}")
    print(f"{actions_input=}")
    return random.random() <= 0.5


def resolve_condition_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    fluents_list: list[QueryFluent],
    timepoint: int,
):
    print(f"{adl_takes_statements=}")
    print(f"{adl_causes_statements=}")
    print(f"{observation_statements=}")
    print(f"{actions_input=}")
    print(f"{fluents_list=}")
    print(f"{timepoint=}")
    return random.random() <= 0.5
