from pytest import fixture

from query_resolution.dto import (
    ActionStatement,
    AdlCausesStatement,
    AdlTakesStatement,
    Fluent,
    ObservationStatement,
)


@fixture(scope="session")
def scenario_1():
    adl_takes_statements = [AdlTakesStatement("LOAD", 3)]

    adl_causes_statements = [
        AdlCausesStatement("LOAD", Fluent("loaded", False), []),
        AdlCausesStatement("SHOOT", Fluent("loaded", True), []),
        AdlCausesStatement(
            "SHOOT", Fluent("alive", True), [Fluent("loaded", False)]
        ),
    ]

    return (
        adl_takes_statements,
        adl_causes_statements,
    )


@fixture(scope="session")
def realization_1_1():
    observation_statements = []

    actions_input = [
        ActionStatement("SHOOT", 1),
        ActionStatement("LOAD", 2),
        ActionStatement("SHOOT", 5),
        ActionStatement("LOAD", 6),
    ]

    time_bound = 10

    return (observation_statements, actions_input, time_bound)


@fixture(scope="session")
def realization_1_2():
    observation_statements = [
        ObservationStatement(Fluent("alive", False), 1),
        ObservationStatement(Fluent("alive", False), 6),
    ]

    actions_input = [
        ActionStatement("SHOOT", 1),
        ActionStatement("LOAD", 2),
        ActionStatement("SHOOT", 5),
    ]

    time_bound = 7

    return (observation_statements, actions_input, time_bound)


@fixture(scope="session")
def realization_1_3():
    observation_statements = []

    actions_input = [
        ActionStatement("SHOOT", 1),
        ActionStatement("LOAD", 2),
        ActionStatement("SHOOT", 5),
    ]

    time_bound = 3

    return (observation_statements, actions_input, time_bound)


@fixture(scope="session")
def realization_1_4():
    observation_statements = []

    actions_input = [
        ActionStatement("SHOOT", 1),
        ActionStatement("LOAD", 2),
        ActionStatement("SHOOT", 4),
    ]

    time_bound = 7

    return (observation_statements, actions_input, time_bound)


@fixture(scope="session")
def scenario_2():
    adl_takes_statements = [
        AdlTakesStatement("STAND UP", 2),
        AdlTakesStatement("SIT DOWN", 2),
    ]

    adl_causes_statements = [
        AdlCausesStatement("STAND UP", Fluent("isStanding", False), []),
        AdlCausesStatement("SIT DOWN", Fluent("isStanding", True), []),
        AdlCausesStatement(
            "SWITH",
            Fluent("on", False),
            [Fluent("isStanding", False), Fluent("on", True)],
        ),
        AdlCausesStatement(
            "SWITH",
            Fluent("on", True),
            [Fluent("isStanding", False), Fluent("on", False)],
        ),
    ]

    return (
        adl_takes_statements,
        adl_causes_statements,
    )


@fixture(scope="session")
def realization_2_1():
    observation_statements = []

    actions_input = [
        ActionStatement("SWITH", 1),
        ActionStatement("SIT DOWN", 2),
        ActionStatement("STAND UP", 4),
        ActionStatement("SWITH", 6),
    ]

    time_bound = 10

    return (observation_statements, actions_input, time_bound)


@fixture(scope="session")
def realization_2_2():
    observation_statements = [ObservationStatement(Fluent("on", False), 4)]

    actions_input = [
        ActionStatement("SWITH", 1),
        ActionStatement("SIT DOWN", 2),
        ActionStatement("STAND UP", 4),
        ActionStatement("SWITH", 6),
    ]

    time_bound = 10

    return (observation_statements, actions_input, time_bound)
