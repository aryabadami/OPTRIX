from language.optrix.lexer import Lexer
from language.optrix.parser import Parser
from language.optrix.semantic.analyzer import (
    SemanticAnalyzer,
    SemanticError,
)


def analyze(source):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()

    SemanticAnalyzer().analyze(program)


def test_defined_variable_is_valid():
    analyze("""let a = 10
let b = a""")


def test_undefined_variable_is_rejected():
    try:
        analyze("let b = a")
    except SemanticError as error:
        assert str(error) == "Undefined variable: a"
    else:
        raise AssertionError(
            "Expected SemanticError for undefined variable"
        )


if __name__ == "__main__":
    test_defined_variable_is_valid()
    test_undefined_variable_is_rejected()

    print("PASS: semantic analyzer tests")


def test_undefined_variable_inside_expression_is_rejected():
    try:
        analyze("""let a = 10
let b = a + c""")
    except SemanticError as error:
        assert str(error) == "Undefined variable: c"
    else:
        raise AssertionError(
            "Expected SemanticError for undefined variable"
        )
