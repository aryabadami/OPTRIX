from lexer.lexer import lex
from parser.parser import parse
from errors import ParserError


def test_invalid_sources():
    sources = [
        "2 +",
        "2 + * 3",
        "(2 + 3",
        "2 + 3)",
        "()",
        "(2 + )",
    ]

    for source in sources:
        try:
            parse(lex(source), source)
        except ParserError as error:
            print(f"PASS: {source!r} -> {error}")
            continue

        raise AssertionError(
            f"Expected ParserError for {source!r}"
        )


def test_error_information():
    source = "2 +"

    try:
        parse(lex(source), source)
    except ParserError as error:
        assert error.phase == "Parser"
        assert error.line == 1
        assert error.column == 4
        assert error.source == source

        print("PASS: ParserError metadata")
        return

    raise AssertionError("Expected ParserError")


def test_token_location_is_used():
    source = "2 + * 3"

    try:
        parse(lex(source), source)
    except ParserError as error:
        assert error.phase == "Parser"
        assert error.line == 1
        assert error.column == 5
        assert "Unexpected token: STAR" in str(error)

        print("PASS: parser uses token location")
        return

    raise AssertionError("Expected ParserError")


def test_source_context():
    source = "2 + * 3"

    try:
        parse(lex(source), source)
    except ParserError as error:
        formatted = str(error)

        assert "2 + * 3" in formatted
        assert "^" in formatted

        print("PASS: parser source context")
        return

    raise AssertionError("Expected ParserError")


def main():
    print("=" * 60)
    print("OPTRIX PARSER ERROR TESTS")
    print("=" * 60)

    test_invalid_sources()
    test_error_information()
    test_token_location_is_used()
    test_source_context()

    print()
    print("ALL PARSER ERROR TESTS PASSED")


if __name__ == "__main__":
    main()
