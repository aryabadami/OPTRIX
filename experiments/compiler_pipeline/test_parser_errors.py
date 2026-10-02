from lexer.lexer import lex
from parser.parser import parse
from errors import ParserError


def test_invalid_sources():
    tests = [
        "2 +",
        "2 + * 3",
        "(2 + 3",
        "2 + 3)",
        "()",
        "(2 + )",
    ]

    for source in tests:
        try:
            parse(lex(source))
        except ParserError as error:
            print(f"PASS: {source!r} -> {error}")
        else:
            raise AssertionError(
                f"Parser accepted invalid source: {source!r}"
            )


def test_error_information():
    try:
        parse(lex("2 +"))
    except ParserError as error:
        assert error.phase == "Parser"
        assert error.line == 1
        assert error.column == 3

        print("PASS: ParserError metadata")
        return

    raise AssertionError(
        "Expected ParserError"
    )


def main():
    print("=" * 60)
    print("OPTRIX PARSER ERROR TESTS")
    print("=" * 60)

    test_invalid_sources()
    test_error_information()

    print()
    print("ALL PARSER ERROR TESTS PASSED")


if __name__ == "__main__":
    main()
