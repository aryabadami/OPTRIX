from language.optrix.lexer import Lexer


def test_lexer_rejects_unknown_character():
    source = "let a = 10 @ 20"

    try:
        Lexer(source).tokenize()
    except SyntaxError as error:
        assert "Unexpected character '@'" in str(error)
    else:
        raise AssertionError("Lexer accepted an unknown character")


if __name__ == "__main__":
    test_lexer_rejects_unknown_character()
    print("PASS: lexer error test")
