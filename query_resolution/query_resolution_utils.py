from query_resolution.dto import (
    ActionStatement,
    AdlCausesStatement,
    AdlTakesStatement,
    Fluent,
)


def get_actions_start_end_dict(
        adl_takes_statements: list[AdlTakesStatement],
        actions_input: list[ActionStatement]
) -> dict[int, int]:
    actions_end_timepoints = {}
    for action in actions_input:
        action_from_adl = None
        for take_statement in adl_takes_statements:
            if action.action == take_statement.action:
                action_from_adl = take_statement
                break
        if action_from_adl is None:
            # by default, an action takes 1 unit of time
            actions_end_timepoints[action.time] = action.time + 1
        else:
            actions_end_timepoints[action.time] = action.time + action_from_adl.time
    return actions_end_timepoints


def match_statements_for_action(takes_statements: list[AdlTakesStatement],
                                causes_statements: list[AdlCausesStatement],
                                action: ActionStatement) -> tuple[AdlTakesStatement, list[AdlCausesStatement]]:
    takes_statement = None
    causes_statement = []
    for statement in takes_statements:
        if statement.action == action.action:
            takes_statement = statement
    for statement in causes_statements:
        if statement.action == action.action:
            causes_statement.append(statement)
    return takes_statement, causes_statement


def change_fluents(current_fluents: list[Fluent], action_statements: list[AdlCausesStatement]) -> list[Fluent]:
    action_with_met_condition_statement = []
    for action_statement in action_statements:
        #if action_with_met_condition_statement is not None:
        #    break
        if len(action_statement.condition_fluents) == 0:
            action_with_met_condition_statement.append(action_statement)
        if len(action_statement.condition_fluents) == 1 and action_statement.condition_fluents[0].name == '':
            action_with_met_condition_statement.append(action_statement)
        else:
            for condition_fluent in action_statement.condition_fluents:
                for fluent in current_fluents:
                    if fluent.name == condition_fluent.name:
                        if fluent.negated == condition_fluent.negated:
                            action_with_met_condition_statement.append(action_statement)
                        else:
                            break
    if len(action_with_met_condition_statement) == 0:
        return current_fluents
    fluents_names_to_change = [action.fluent.name for action in action_with_met_condition_statement]
    fluents_to_change = [action.fluent for action in action_with_met_condition_statement]
    new_fluents = [0 for i in range(len(current_fluents))]
    for i in range(len(current_fluents)):
        if current_fluents[i].name not in fluents_names_to_change:
            new_fluents[i] = current_fluents[i]
        else:
            for j in range(len(fluents_names_to_change)):
                if current_fluents[i].name == fluents_names_to_change[j]:
                    new_fluents[i] = fluents_to_change[j]
    return new_fluents


def get_fluents_names_from_causes_statements(causes_statements: list[AdlCausesStatement]) -> list[str]:
    fluents = [statement.fluent.name for statement in causes_statements]
    return list(set(fluents))

