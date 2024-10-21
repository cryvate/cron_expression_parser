import pytest

import cron_expression_parser

EXPECTED_OUTPUT = """minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
"""


# IMP: the formatting/processing functions are untested


# IMP: as mentioned elsewhere, error handling should be changed in general
@pytest.mark.parametrize(
    "token",
    [
        "foo",
        "60",
        "0-60",
        "/1",
        "0-30/*",
    ],
)
def test_parse_token_invalid_raise_exception(token):
    with pytest.raises(Exception):
        cron_expression_parser.parse_token(token, 0, 59)


@pytest.mark.parametrize(
    "token, output",
    [
        ("5", [5]),
        ("5-10", [5, 6, 7, 8, 9, 10]),
        ("*/10", [0, 10, 20, 30, 40, 50]),
        ("5-20/10", [5, 15]),
    ],
)
def test_parse_token(token: str, output: list[int]):
    assert list(cron_expression_parser.parse_token(token, 0, 59)) == output


@pytest.mark.parametrize(
    "string, output", [("5", [5]), ("5,5,5", [5]), ("5,4,3", [3, 4, 5])]
)
def test_parse_tokens(string, output):
    tokens = string.split(cron_expression_parser.SEPARATOR)
    assert cron_expression_parser.parse_tokens(tokens, 0, 59) == output


def test_main(capsys):
    cron_expression_parser.main("*/15 0 1,15 * 1-5 /usr/bin/find")
    captured = capsys.readouterr()
    assert captured.out == EXPECTED_OUTPUT
