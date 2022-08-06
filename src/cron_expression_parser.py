import sys
import typing

# IMP: would be split into multiple files, but this (it being in one file)
# might make iterating easier in interview
ORDER = {
    "minute": (0, 59),
    "hour": (0, 23),
    "day of month": (0, 31),
    "month": (1, 12),
    "day of week": (1, 7),
}
COMMAND = "command"
SPACING = 2
PAD = len(max(*ORDER, COMMAND, key=lambda string: len(string))) + SPACING
WILDCARD = "*"
SEPARATOR = ","
STEP = "/"
RANGE = "-"
EMPTY_SPACE = " "


# IMP this function and others will bail out when a bad
# expression is given with little diagnostics. This
# is not great UX, would improve this
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
    match token.split(STEP, maxsplit=1):
        case [token, repeated_string]:
            repeated = int(repeated_string)
        case [token]:
            repeated = 1

    if "*" == token:
        begin = minimum
        end = maximum
    elif "-" in token:
        begin_str, end_str = token.split(RANGE, maxsplit=1)
        begin = int(begin_str)
        end = int(end_str)
    else:
        begin = int(token)
        end = int(token)

    if begin < minimum:
        raise ValueError()
    if end > maximum:
        raise ValueError()

    return range(begin, end + 1, repeated)


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
    for column, values in row_data:
        preamble = column.ljust(PAD)
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
