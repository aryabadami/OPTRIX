from language.optrix.lexer import Lexer
from language.optrix.tokens import TokenType


def test_lexer_tokenizes_basic_program():
    source = """let a = 10
let b = 20
let c = a + b"""

    tokens = Lexer(source).tokenize()

    token_types = [token.type for token in tokens]

    assert token_types == [
        TokenType.LET,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.INTEGER,
        TokenType.NEWLINE,

        TokenType.LET,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.INTEGER,
        TokenType.NEWLINE,

        TokenType.LET,
        TokenType.IDENTIFIER,
        TokenType.EQUAL,
        TokenType.IDENTIFIER,
        TokenType.PLUS,
        TokenType.IDENTIFIER,

        TokenType.EOF,
    ]


def test_lexer_preserves_lexemes():
    source = "let answer = 42"

    tokens = Lexer(source).tokenize()

    assert [token.lexeme for token in tokens] == [
        "let",
        "answer",
        "=",
        "42",
        "",
    ]


if __name__ == "__main__":
    test_lexer_tokenizes_basic_program()
    test_lexer_preserves_lexemes()
    print("PASS: lexer tests")
