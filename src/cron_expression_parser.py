import sys
import typing

# IMP: would be split into multiple files, but this (it being in one file)
# might make iterating easier in interview

# IMP: I love using constants, I don't like magic numbers in source that are not
#      defined, even for things that seem stupid to abstract (e.g. the
#      EMPTY_SPACE). The benefit is having a single-source-of-truth, which
#      I have seen lead to so many bugs/regressions when things are changed,
#      even when we're talking small numbers/chars like 0, 1, 2 and "-".
#      It can also help with semantic separation (like units in physics)
#      between two constants that are accidentally the same
ORDER = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day of month": (0, 31),
    "month": (1, 12),
    "day of week": (1, 7),
}
COMMAND = "command"
PADDING = 2
WILDCARD = "*"
SEPARATOR = ","
STEP = "/"
RANGE = "-"
EMPTY_SPACE = " "


# IMP: this function and others will bail out when a bad
#      expression is given with little diagnostics. This
#      is not great UX, would improve this
def parse_token(
    token: str,
    minimum: int,
    maximum: int,
) -> typing.Iterable[int]:
    """
    :param token: a token expressing values: "0-8" or "*/5" but not "0,5"
    :param minimum: minimum value (inclusive) that is valid for this unit
    :param maximum: maximum value (inclusive) that is valid for this unit
    :return: an iterable that contains all the valid values for this token
    """
    # split the token between the
    match token.split(STEP, maxsplit=1):
        case [start_end, step_string]:
            step = int(step_string)
        case [start_end]:
            step = 1
        case _:
            # This path cannot be triggered. Helpful for type checking/linting
            raise Exception("This should not be seen...")

    if "*" == start_end:
        begin = minimum
        end = maximum
    elif "-" in start_end:
        begin_str, end_str = start_end.split(RANGE, maxsplit=1)
        begin = int(begin_str)
        end = int(end_str)
    else:
        begin = int(start_end)
        end = int(start_end)

    if begin < minimum:
        # IMP: this should have a sane message, but also, error handling needs
        #      more thought in general
        raise ValueError()
    if end > maximum:
        # IMP: same as above
        raise ValueError()

    return range(begin, end + 1, step)


def parse_tokens(
    tokens: typing.Iterable[str],
    minimum: int,
    maximum: int,
) -> list[int]:
    """
    :param tokens: an iterable of tokens, see `token_to_concrete_values`
    :param minimum: minimum value (inclusive) that is valid for this unit
    :param maximum: maximum value (inclusive) that is valid for this unit
    :return: sorted valid values for this group
    """
    valid: set[int] = set()
    for part in tokens:
        valid.update(
            parse_token(
                part,
                minimum,
                maximum,
            )
        )
    return sorted(valid)


def parse(command: list[str]) -> list[tuple[str, list[int]]]:
    """
    Parse a full cron expression

    :param command: the cron expression split by whitespace
    :return: tuples of (unit, valid-values-in-unit)
    """
    return [
        (
            key,
            parse_tokens(
                subcommand.split(SEPARATOR),
                minimum_value,
                maximum_value,
            ),
        )
        for subcommand, (key, (minimum_value, maximum_value)) in zip(
            command, ORDER.items()
        )
    ]


# IMP: in theory, we don't need to pass tuple[str, X] around
#      in this function and the ones below: instead could use
#      X instead and use the keys from ORDER, however, this is
#      not necessarily great design or robust for generalisation
#      e.g. we currently don't support year, and this is optional
#      in the cron "spec" from what I can tell so you would only
#      want to output that line if present and also if this code
#      was reused for other CLIs. I like the decoupling it brings
#      between these functions
def parsed_to_display_data(
    parsed: typing.Iterable[tuple[str, list[int]]]
) -> list[tuple[str, str]]:
    """
    :param parsed: parsed cron expression
    :return: tuples of (header, valid values formatted)
    """
    return [
        (key, EMPTY_SPACE.join(str(value) for value in values))
        for key, values in parsed
    ]


def format_lines(row_data: typing.Iterable[tuple[str, str]]) -> str:
    """
    Helper functions that makes pretty-ish formatted two column data

    :param row_data: containing the row data, and the headers should be
                     from the set we expect (ORDER.keys() + COMMAND)
    :return: formatted two column data
    """
    lines = []

    # IMP: I don't like this, all the rest of the functions work on-line,
    #      and could be changed to use e.g. generators, yield (from) and
    #      send, but this doesn't. Originally I calculated this statically
    #      but this tightly couples this function to this particular instance
    #      of the generic problem which seems unnecessary.
    width = len(max(row_data, key=lambda header, _: len(header))) + PADDING

    for column, values in row_data:
        preamble = column.ljust(width)
        values_string = (str(value) for value in values.split(SEPARATOR))
        values = EMPTY_SPACE.join(values_string)
        lines.append(preamble + values)

    return "\n".join(lines)


def main(expression: str) -> None:
    """
    :param expression: cron expression to be parsed
    """
    arguments = expression.split()
    command = arguments.pop()
    parsed = parse(arguments)
    display_data = parsed_to_display_data(parsed)
    display_data.append((COMMAND, command))
    output = format_lines(display_data)
    print(output)


# IMP: should be wrapped with something to turn it into
# a proper CLI
def run() -> None:
    """
    Entrypoint for script, including for packaging
    """
    main(sys.argv[1])


if __name__ == "__main__":
    run()
