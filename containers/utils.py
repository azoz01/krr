from query_resolution.dto import Fluent


def parse_fluent_from_string(string) -> Fluent:
    string = string.strip()
    negated = "not" in string
    fluent = string if not negated else string.split(" ")[1]
    return Fluent(name=fluent, negated=negated)
