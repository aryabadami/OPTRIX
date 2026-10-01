from lexer.lexer import lex, Token
from errors import LexerError


def test_valid_source():
    tokens = lex("2 + 3")

    assert tokens[0] == Token(
        "NUMBER",
        "2",
    )

    assert tokens[1] == Token(
        "PLUS",
        "+",
    )

    assert tokens[2] == Token(
        "NUMBER",
        "3",
    )

    assert tokens[3] == Token(
        "EOF",
        "",
    )

    print("PASS: valid source")


def test_parentheses():
    tokens = lex("(2 + 3)")

    kinds = [
        token.kind
        for token in tokens
    ]

    assert kinds == [
        "LPAREN",
        "NUMBER",
        "PLUS",
        "NUMBER",
        "RPAREN",
        "EOF",
    ]

    print("PASS: parentheses")


def test_invalid_character():
    try:
        lex("2 @ 3")
    except LexerError as error:
        assert error.phase == "Lexer"
        assert error.line == 1
        assert error.column == 3

        print("PASS: invalid character")
        return

    raise AssertionError(
        "Lexer accepted invalid character"
    )


def test_multiple_invalid_characters():
    invalid_sources = [
        "2 # 3",
        "2 $ 3",
        "2 & 3",
        "2 = 3",
        "2 % 3",
    ]

    for source in invalid_sources:
        try:
            lex(source)
        except LexerError:
            print(
                f"PASS: rejected {source!r}"
            )
        else:
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

    raise AssertionError(
        "Expected LexerError"
    )


def main():
    print("=" * 60)
    print("OPTRIX LEXER ERROR TESTS")
    print("=" * 60)

    test_valid_source()
    test_parentheses()
    test_invalid_character()
    test_multiple_invalid_characters()
    test_error_message()

    print()
    print("=" * 60)
    print("ALL LEXER ERROR TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
