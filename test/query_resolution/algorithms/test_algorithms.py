import pytest

from containers.utils import ContradictiveLanguageException
from query_resolution.algorithms import (
    resolve_condition_query,
    resolve_realizable_query,
)
from query_resolution.dto import Fluent


def test_example_1_1(scenario_1, realization_1_1):

    adl_takes_statements, adl_causes_statements = scenario_1
    observation_statements, actions_input, time_bound = realization_1_1

    is_realizable = resolve_realizable_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        time_bound,
    )[0]

    is_true_1 = resolve_condition_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        [Fluent("alive", True)],
        6,
        time_bound,
    )

    is_true_2 = resolve_condition_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        [Fluent("loaded", True)],
        2,
        time_bound,
    )

    assert is_realizable
    assert is_true_1
    assert is_true_2


def test_example_1_2(scenario_1, realization_1_2):

    adl_takes_statements, adl_causes_statements = scenario_1
    observation_statements, actions_input, time_bound = realization_1_2

    is_realizable = resolve_realizable_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        time_bound,
    )[0]

    assert not is_realizable


def test_example_1_3(scenario_1, realization_1_3):

    adl_takes_statements, adl_causes_statements = scenario_1
    observation_statements, actions_input, time_bound = realization_1_3

    is_realizable = resolve_realizable_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        time_bound,
    )[0]

    assert not is_realizable


def test_example_1_4(scenario_1, realization_1_4):

    adl_takes_statements, adl_causes_statements = scenario_1
    observation_statements, actions_input, time_bound = realization_1_4

    is_realizable = resolve_realizable_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        time_bound,
    )[0]

    assert not is_realizable


def test_example_2_1(scenario_2, realization_2_1):

    adl_takes_statements, adl_causes_statements = scenario_2
    observation_statements, actions_input, time_bound = realization_2_1

    is_realizable = resolve_realizable_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        time_bound,
    )[0]

    is_true_1 = resolve_condition_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        [Fluent("on", True)],
        7,
        time_bound,
    )

    is_true_2 = resolve_condition_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        [Fluent("isStanding", True)],
        4,
        time_bound,
    )

    is_true_3 = resolve_condition_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        [Fluent("isStanding", True)],
        5,
        time_bound,
    )

    assert is_realizable

    assert not is_true_1
    assert is_true_2
    assert not is_true_3


def test_example_2_2(scenario_2, realization_2_2):

    adl_takes_statements, adl_causes_statements = scenario_2
    observation_statements, actions_input, time_bound = realization_2_2

    is_realizable = resolve_realizable_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        time_bound,
    )[0]

    is_true_1 = resolve_condition_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        [Fluent("on", True)],
        7,
        time_bound,
    )

    assert is_realizable

    assert is_true_1


def test_example_0(scenario_0, realization_0_0):
    adl_takes_statements, adl_causes_statements = scenario_0
    observation_statements, actions_input, time_bound = realization_0_0

    with pytest.raises(ContradictiveLanguageException):
        _ = resolve_realizable_query(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
            time_bound,
        )
