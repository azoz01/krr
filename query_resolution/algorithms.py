from itertools import product

from query_resolution.dto import (
    ActionStatement,
    AdlCausesStatement,
    AdlTakesStatement,
    Fluent,
    ObservationStatement,
)
from query_resolution.query_resolution_utils import (
    change_fluents,
    get_actions_start_end_dict,
    get_fluents_names_from_causes_statements,
    match_statements_for_action,
)
from containers.utils import ContradictiveLanguageException


def resolve_realizable_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    time_bound: int,
) -> tuple[bool, list[list[Fluent]]]:
    """
    :param adl_takes_statements: list of ADL 'TAKES' statements
    :param adl_causes_statements: list of ADL 'CAUSES statements
    :param observation_statements: list of observations for the scenario
    :param actions_input: list of actions performed during the scenario
    :param time_bound: timepoint before which all actions must be terminated
    :return: True and a list of possible initial fluents if the scenario is realizable, else False and an empty list
    This function checks if the scenario is realizable.
    """
    # check if causes statements do not contradict
    for action in adl_causes_statements:
        for action_1 in adl_causes_statements:
            if action != action_1 and action.action == action_1.action:
                fluent, fluent_1 = action.fluent, action_1.fluent
                if fluent.name == fluent_1.name and fluent.negated != fluent_1.negated:
                    for cond_fluent in action.condition_fluents:
                        if cond_fluent.name not in [cond_fluent1.name for cond_fluent1 in action_1.condition_fluents]:
                            raise ContradictiveLanguageException(
                                'Actions defined in Causes statements cannot contradict each other!'
                            )
    # check if takes statements do not contradict
    unique_actions_dict = {}
    for action in adl_takes_statements:
        if action.action not in list(unique_actions_dict.keys()):
            unique_actions_dict[action.action] = action.time
        else:
            if action.time != unique_actions_dict.get(action.action):
                raise ContradictiveLanguageException(
                    'There cannot be two ADL TAKES statements for the same action with different times!'
                )
    # create a takes statement with time 1 if no takes statement specified for action
    adl_takes_actions = [statement.action for statement in adl_takes_statements]
    for action in actions_input:
        if action.action not in adl_takes_actions:
            adl_takes_actions.append(action.action)
            adl_takes_statements.append(AdlTakesStatement(action=action.action, time=1))
    actions_start_end_timepoints = get_actions_start_end_dict(
        adl_takes_statements, actions_input
    )
    # check if all actions terminate before the termination timepoint:
    if max(list(actions_start_end_timepoints.values())) > time_bound:
        return False, []
    # check if any actions overlap:
    sorted_actions_timepoints = sorted(actions_start_end_timepoints.items())
    for i in range(len(sorted_actions_timepoints) - 1):
        if (
            sorted_actions_timepoints[i][1]
            > sorted_actions_timepoints[i + 1][0]
        ):
            return False, []
        # no inconsistencies can be found if no actions are passed as inputs
    # get all possible initial states regarding the fluents from observations
    fluent_names = get_fluents_names_from_causes_statements(
        adl_causes_statements
    )
    negated_combinations = product([True, False], repeat=len(fluent_names))
    possible_initial_fluents = []
    for negated_values in negated_combinations:
        possible_initial_fluents.append(
            (
                [
                    Fluent(name, negated)
                    for name, negated in zip(fluent_names, negated_values)
                ]
            )
        )
    if len(observation_statements) == 0:
        return True, possible_initial_fluents
    initial_fluents = []
    for element in possible_initial_fluents:
        if scenario_realizable_for_specific_model(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
            element,
        ):
            initial_fluents.append(element)
    if len(initial_fluents) == 0:
        return False, []
    # it is sufficient if a single model is correct
    return True, initial_fluents


def resolve_condition_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    fluents_list: list[Fluent],
    timepoint: int,
    time_bound: int,
) -> bool:
    """
    :param adl_takes_statements: list of ADL 'TAKES' statements
    :param adl_causes_statements: list of ADL 'CAUSES statements
    :param observation_statements: list of observations for the scenario
    :param actions_input: list of actions performed during the scenario
    :param fluents_list: list of fluents conditioned to be held at timepoint
    :param timepoint: timepoint for condition fluents
    :param time_bound: timepoint before which all actions must be terminated
    :return: True if the conditions are held, esle False
    This function firstly checks if the scenario is realizable. If so, for each possible initial fluents from the
    scenario it checks whether the specified fluents are held at the specified timepoint. If they are not held for at
    least one set of initial fluents, the function returns False, else True
    """
    realizable, possible_initial_fluents = resolve_realizable_query(
        adl_takes_statements,
        adl_causes_statements,
        observation_statements,
        actions_input,
        time_bound
    )
    if not realizable:
        return False
    for element in possible_initial_fluents:
        if not conditions_met_for_specific_model(
            adl_takes_statements,
            adl_causes_statements,
            actions_input,
            element,
            fluents_list,
            timepoint,
        ):
            return False
    return True


def scenario_realizable_for_specific_model(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    initial_fluents: list[Fluent],
) -> bool:
    """
    :param adl_takes_statements: list of ADL 'TAKES' statements
    :param adl_causes_statements: list of ADL 'CAUSES statements
    :param observation_statements: list of observations for the scenario
    :param actions_input: list of actions performed during the scenario
    :param initial_fluents: list of initial fluents for this model
    :return: True if the scenario for the specified model is realizable, else False
    This function checks if for given initial fluents the scenario can be realised
    """
    # for now, the assumption is that the user inputs actions in a correct order
    current_timepoint = actions_input[0].time
    current_fluents = initial_fluents
    for action in actions_input:
        takes_statement, causes_statements = match_statements_for_action(
            adl_takes_statements, adl_causes_statements, action
        )
        next_timepoint = current_timepoint + takes_statement.time
        # if the action changing the fluent is performing, we do not know the fluents' state
        for observation in observation_statements:
            for causes_statement in causes_statements:
                if (
                    current_timepoint < observation.time < next_timepoint
                    and observation.fluent == causes_statement.fluent
                ):
                    return False
        current_timepoint = next_timepoint
        current_fluents = change_fluents(current_fluents, causes_statements)
        for observation in observation_statements:
            if observation.time == current_timepoint:
                for fluent in current_fluents:
                    if observation.fluent.name == fluent.name:
                        if observation.fluent.negated != fluent.negated:
                            return False
    return True


def conditions_met_for_specific_model(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    actions_input: list[ActionStatement],
    initial_fluents: list[Fluent],
    condition_fluents: list[Fluent],
    timepoint: int,
) -> bool:
    """
    :param adl_takes_statements: list of ADL 'TAKES' statements
    :param adl_causes_statements: list of ADL 'CAUSES statements
    :param actions_input: list of actions performed during the scenario
    :param initial_fluents: list of initial fluents for this model
    :param condition_fluents: list of fluents conditioned to be held at timepoint
    :param timepoint: timepoint for condition fluents
    :return: True if the condition is met for the model specified with input, else False
    This function checks if the fluents that were asked in a query are held at a timepoint
    """
    # for now, the assumption is that the user inputs actions in a correct order
    current_timepoint = actions_input[0].time
    current_fluents = initial_fluents
    if timepoint == current_timepoint:
        for fluent in condition_fluents:
            for current_fluent in current_fluents:
                if fluent.name == current_fluent.name:
                    if fluent.negated != current_fluent.negated:
                        return False
    for action in actions_input:
        takes_statement, causes_statements = match_statements_for_action(
            adl_takes_statements, adl_causes_statements, action
        )
        next_timepoint = current_timepoint + takes_statement.time
        # if the action changing the fluent is performing, we do not know the fluents' state
        for fluent in condition_fluents:
            for causes_statement in causes_statements:
                if (
                    current_timepoint < timepoint < next_timepoint
                    and fluent.name == causes_statement.fluent.name
                ):
                    return False
        current_timepoint = next_timepoint
        current_fluents = change_fluents(current_fluents, causes_statements)
        if timepoint == current_timepoint:
            for fluent in condition_fluents:
                for current_fluent in current_fluents:
                    if fluent.name == current_fluent.name:
                        if fluent.negated != current_fluent.negated:
                            return False
    return True


def _test() -> None:
    time_bound = 15
    adl_takes_statements = [
        AdlTakesStatement(action="STAND_UP", time=2),
        AdlTakesStatement(action="SIT_DOWN", time=2),
        AdlTakesStatement(action="SWITCH", time=1),
    ]
    adl_causes_statements = [
        AdlCausesStatement(
            action="STAND_UP",
            fluent=Fluent(name="standing", negated=False),
            condition_fluents=[],
        ),
        AdlCausesStatement(
            action="SIT_DOWN",
            fluent=Fluent(name="standing", negated=True),
            condition_fluents=[],
        ),
        AdlCausesStatement(
            action="SWITCH",
            fluent=Fluent("on", False),
            condition_fluents=[Fluent("standing", False), Fluent("on", True)],
        ),
        AdlCausesStatement(
            action="SWITCH",
            fluent=Fluent("on", True),
            condition_fluents=[Fluent("standing", False), Fluent("on", False)],
        ),
    ]
    observation_statements = []
    actions_input = [
        ActionStatement(action="SWITCH", time=1),
        ActionStatement(action="SIT_DOWN", time=2),
        ActionStatement(action="STAND_UP", time=4),
        ActionStatement(action="SWITCH", time=6),
    ]
    print(
        resolve_realizable_query(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
            time_bound,
        )
    )
    print(
        resolve_condition_query(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
            [Fluent("on", False)],
            7,
            time_bound,
        )
    )
    print(
        resolve_condition_query(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
            [Fluent("standing", True)],
            4,
            time_bound,
        )
    )
    print(
        resolve_condition_query(
            adl_takes_statements,
            adl_causes_statements,
            observation_statements,
            actions_input,
            [Fluent("standing", False)],
            6,
            time_bound,
        )
    )


if __name__ == "__main__":
    _test()
