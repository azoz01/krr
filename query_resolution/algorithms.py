import random
from itertools import product

from query_resolution.dto import (
    ActionStatement,
    AdlCausesStatement,
    AdlTakesStatement,
    Fluent,
    ObservationStatement,
)

from query_resolution.query_resolution_utils import (
    get_actions_start_end_dict,
    match_statements_for_action,
    change_fluents,
    get_fluents_names_from_causes_statements
)

TEMP_FIXED_TERMINATION_POINT = 15


def resolve_realizable_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
) -> bool:
    actions_start_end_timepoints = get_actions_start_end_dict(adl_takes_statements, actions_input)
    # check if all actions terminate before the termination timepoint:
    if max(list(actions_start_end_timepoints.values())) > TEMP_FIXED_TERMINATION_POINT:
        return False
    # check if any actions overlap:
    sorted_actions_timepoints = sorted(actions_start_end_timepoints.items())
    for i in range(len(sorted_actions_timepoints) - 1):
        if sorted_actions_timepoints[i][1] > sorted_actions_timepoints[i+1][0]:
            return False
        # no inconsistencies ca be found if no actions are passed as inputs
    if len(observation_statements) == 0:
        return True
    # get all possible initial states regarding the fluents from observations
    initial_fluent_states = []
    for observation in observation_statements:
        if observation.time == 0:
            initial_fluent_states.append(observation.fluent)
        else:
            initial_fluent_states.append(observation.fluent.negated)
            initial_fluent_states.append(not observation.fluent.negated)
    fluent_names = get_fluents_names_from_causes_statements(adl_causes_statements)
    negated_combinations = product([True, False], repeat=len(fluent_names))
    possible_initial_fluents = []
    for negated_values in negated_combinations:
        possible_initial_fluents.append(([Fluent(name, negated) for name, negated in zip(fluent_names, negated_values)]))
    for element in possible_initial_fluents:
        # it is sufficient if a single model is correct
        if scenario_realizable_for_specific_model(adl_takes_statements, adl_causes_statements, observation_statements,
                                                  actions_input, element):
            return True
    return False


def resolve_condition_query(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    fluents_list: list[Fluent],
    timepoint: int,
):
    actions_start_end_timepoints = get_actions_start_end_dict(adl_takes_statements, actions_input)
    fluents_names = [fluent.name for fluent in fluents_list]
    fluents_names = list(set(fluents_names))
    negated_combinations = product([True, False], repeat=len(fluents_names))
    possible_initial_fluents = []
    for negated_values in negated_combinations:
        possible_initial_fluents.append(
            ([Fluent(name, negated) for name, negated in zip(fluents_names, negated_values)]))
    for element in possible_initial_fluents:
        if not conditions_met_for_specific_model(adl_takes_statements, adl_causes_statements,
                                                 actions_input, element, fluents_list, timepoint):
            return False
    return True


def scenario_realizable_for_specific_model(
    adl_takes_statements: list[AdlTakesStatement],
    adl_causes_statements: list[AdlCausesStatement],
    observation_statements: list[ObservationStatement],
    actions_input: list[ActionStatement],
    initial_fluents: list[Fluent]
):
    # for now, the assumption is that the user inputs actions in a correct order
    current_timepoint = actions_input[0].time
    current_fluents = initial_fluents
    for action in actions_input:
        takes_statement, causes_statement = match_statements_for_action(adl_takes_statements, adl_causes_statements,
                                                                        action)
        current_timepoint += takes_statement.time
        current_fluents = change_fluents(current_fluents, causes_statement)
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
    timepoint: int
):
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
        takes_statement, causes_statement = match_statements_for_action(adl_takes_statements, adl_causes_statements,
                                                                        action)
        current_timepoint += takes_statement.time
        current_fluents = change_fluents(current_fluents, causes_statement)
        if timepoint == current_timepoint:
            for fluent in condition_fluents:
                for current_fluent in current_fluents:
                    if fluent.name == current_fluent.name:
                        if fluent.negated != current_fluent.negated:
                            return False
    return True




def _test():
    adl_takes_statements = [AdlTakesStatement(action='LOAD', time=3), AdlTakesStatement(action='SHOOT', time=1)]
    adl_causes_statements = [AdlCausesStatement(action='SHOOT', fluent=Fluent(name='loaded', negated=True),
                                                condition_fluents=[]),
                             AdlCausesStatement(action='SHOOT', fluent=Fluent(name='alive', negated=True),
                                                condition_fluents=[Fluent(name='loaded', negated=False)]),
                             AdlCausesStatement(action='LOAD', fluent=Fluent('loaded', False),
                                                condition_fluents=[])]
    observation_statements = [ObservationStatement(fluent=Fluent(name='alive', negated=True), time=5),
                              ObservationStatement(fluent=Fluent(name='loaded', negated=False), time=1)]
    actions_input = [ActionStatement(action='LOAD', time=1), ActionStatement(action='SHOOT', time=4)]
    print(resolve_condition_query(adl_takes_statements, adl_causes_statements, observation_statements, actions_input,
                                  [Fluent('loaded', False)], 4))


if __name__ == '__main__':
    _test()
