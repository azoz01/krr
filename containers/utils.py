from query_resolution.dto import Fluent


def parse_fluent_from_string(string) -> Fluent:
    string = string.strip()
    negated = "not" in string
    fluent = string if not negated else string.split(" ")[1]
    return Fluent(name=fluent, negated=negated)


class GlobalValueHolder:

    def __init__(self, val):
        self.val = val


HELP_TEXT = """
This is an application that answers queries corresponding to Action Description Language
analogous to AL. It takes statements from action description language and scenario i.e.
observations and actions.

General remarks:
    * To add a new entry in input columns click the '+' button.
    * To remove entry click the '-' icon which corresponds to this entry.
    * Provided times must be non-negative integers.
    * To provide negated fluent 'f' type 'not f'.
    * A set of actions and fluents are extracted from ADL definition so there
        is no need to declare them explicitly.

Input:
    * To provide 'A takes t' statements from ADL input them to the upper field in the first column.
        In the first text field provide the name of the action 'A' and in the second time 't'.
    * To provide 'A causes f if f1, f2, ...' statements from ADL input them to the bottom field in
        the first column. In the first text field provide the name of the action 'A' and in the second
        fluent 'f'. In the last field provide a comma-separated list of fluents (or their negations).
        To make no condition on statement (A casuses f if T), left the last field empty.
    * To provide observations (f, t) from the scenario input them to the field in the second column. In the
        first text field provide the name of the fluent 'f' and in the second time 't'.
    * To provide actions (A, t) from the scenario input them to the field in the third column. In the first
        text field provide the name of the action 'A' and in the second time 't'.
    * To provide an upper time bound for the scenario, provide it in the text input in the upper right corner.

Query:
    * To run a query about applicability, click 'Run' next to "Is scenario realizable?". Note, that it does
        not require additional information.
    * To run a query about conditions, click 'Run' next to "Does set of fluents hold at t?". To provide timepoint
        't' input it to the 'Timepoint' input field. To provide fluents provide them in the list in the lower bottom corner.
"""


class ContradictiveLanguageException(Exception):
    def __init__(self, message):
        self.message = message
