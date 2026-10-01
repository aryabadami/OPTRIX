from language.optrix.tokens import Token, TokenType


def test_token_types_exist():
    assert TokenType.LET
    assert TokenType.IDENTIFIER
    assert TokenType.INTEGER
    assert TokenType.EQUAL
    assert TokenType.PLUS
    assert TokenType.MINUS
    assert TokenType.STAR
    assert TokenType.SLASH
    assert TokenType.EOF


def test_token_preserves_source_information():
    token = Token(
        TokenType.IDENTIFIER,
        "answer",
        3,
        5,
    )

    assert token.type is TokenType.IDENTIFIER
    assert token.lexeme == "answer"
    assert token.line == 3
    assert token.column == 5


if __name__ == "__main__":
    test_token_types_exist()
    test_token_preserves_source_information()
    print("PASS: token model tests")
