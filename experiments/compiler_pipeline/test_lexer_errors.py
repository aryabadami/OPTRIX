from lexer.lexer import lex, Token
from errors import LexerError


def test_valid_source():
    tokens = lex("2 + 3")

    assert tokens[0] == Token(
        "NUMBER",
        "2",
        line=1,
        column=1,
    )

    assert tokens[1] == Token(
        "PLUS",
        "+",
        line=1,
        column=3,
    )

    assert tokens[2] == Token(
        "NUMBER",
        "3",
        line=1,
        column=5,
    )

    assert tokens[3] == Token(
        "EOF",
        "",
        line=1,
        column=6,
    )

    print("PASS: valid source")


def test_parentheses():
    tokens = lex("(2 + 3)")

    assert tokens[0].kind == "LPAREN"
    assert tokens[0].value == "("
    assert tokens[0].line == 1
    assert tokens[0].column == 1

    assert tokens[1].kind == "NUMBER"
    assert tokens[1].value == "2"
    assert tokens[1].line == 1
    assert tokens[1].column == 2

    assert tokens[2].kind == "PLUS"
    assert tokens[2].value == "+"
    assert tokens[2].line == 1
    assert tokens[2].column == 4

    assert tokens[3].kind == "NUMBER"
    assert tokens[3].value == "3"
    assert tokens[3].line == 1
    assert tokens[3].column == 6

    assert tokens[4].kind == "RPAREN"
    assert tokens[4].value == ")"
    assert tokens[4].line == 1
    assert tokens[4].column == 7

    assert tokens[5].kind == "EOF"
    assert tokens[5].line == 1
    assert tokens[5].column == 8

    print("PASS: parentheses")


def test_invalid_character():
    try:
        lex("2 # 3")
    except LexerError:
        print("PASS: invalid character")
        return

    raise AssertionError("Expected LexerError")


def test_multiple_invalid_characters():
    sources = [
        "2 # 3",
        "2 $ 3",
        "2 & 3",
        "2 = 3",
        "2 % 3",
    ]

    for source in sources:
        try:
            lex(source)
        except LexerError:
            print(f"PASS: rejected {source!r}")
            continue

        raise AssertionError(
            f"Accepted invalid source: {source!r}"
        )


def test_error_message():
    try:
        lex("10 + @")
    except LexerError as error:
        text = str(error)

        assert "[Lexer]" in text
        assert "Unexpected character" in text
        assert "'@'" in text
        assert "line 1" in text
        assert "column 6" in text

        print("PASS: lexer diagnostic")
        return

    raise AssertionError("Expected LexerError")


def test_multiline_locations():
    tokens = lex("12 + 3\n45 * 6")

    assert tokens[0].line == 1
    assert tokens[0].column == 1

    assert tokens[1].line == 1
    assert tokens[1].column == 4

    assert tokens[2].line == 1
    assert tokens[2].column == 6

    assert tokens[3].line == 2
    assert tokens[3].column == 1

    assert tokens[4].line == 2
    assert tokens[4].column == 4

    assert tokens[5].line == 2
    assert tokens[5].column == 6

    assert tokens[6].kind == "EOF"
    assert tokens[6].line == 2
    assert tokens[6].column == 7

    print("PASS: multiline token locations")


def main():
    print("=" * 60)
    print("OPTRIX LEXER ERROR TESTS")
    print("=" * 60)

    test_valid_source()
    test_parentheses()
    test_invalid_character()
    test_multiple_invalid_characters()
    test_error_message()
    test_multiline_locations()

    print()
    print("ALL LEXER ERROR TESTS PASSED")


if __name__ == "__main__":
    main()
