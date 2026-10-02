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


def test_integer_type_is_inferred():
    tokens = Lexer("""let a = 10
let b = a""").tokenize()

    program = Parser(tokens).parse_program()

    analyzer = SemanticAnalyzer()
    analyzer.analyze(program)

    from language.optrix.semantic.types import INTEGER

    assert analyzer.symbols.get_type("a") == INTEGER
    assert analyzer.symbols.get_type("b") == INTEGER


def test_boolean_type_is_inferred():
    tokens = Lexer("""let flag = true
let other = flag""").tokenize()

    program = Parser(tokens).parse_program()

    analyzer = SemanticAnalyzer()
    analyzer.analyze(program)

    from language.optrix.semantic.types import BOOLEAN

    assert analyzer.symbols.get_type("flag") == BOOLEAN
    assert analyzer.symbols.get_type("other") == BOOLEAN


def test_integer_and_boolean_cannot_be_added():
    try:
        analyze("""let a = 10
let b = true
let c = a + b""")
    except SemanticError as error:
        assert str(error) == "Operator '+' requires integer operands"
    else:
        raise AssertionError(
            "Expected SemanticError for Integer + Boolean"
        )


if __name__ == "__main__":
    test_defined_variable_is_valid()
    test_undefined_variable_is_rejected()
    test_undefined_variable_inside_expression_is_rejected()
    test_integer_type_is_inferred()
    test_boolean_type_is_inferred()
    test_integer_and_boolean_cannot_be_added()

    print("PASS: semantic analyzer tests")


def test_undefined_variable_error_has_location():
    try:
        analyze("let b = a")
    except SemanticError as error:
        from language.optrix.source import SourceLocation

        assert error.location == SourceLocation(line=1, column=9)
    else:
        raise AssertionError(
            "Expected SemanticError for undefined variable"
        )


def test_comparison_expressions_return_boolean():
    for source in [
        "10 < 20",
        "10 > 20",
        "10 == 20",
        "10 != 20",
    ]:
        expression = Parser(
            Lexer(source).tokenize()
        ).parse_expression()

        result = SemanticAnalyzer()._analyze_expression(expression)

        assert result == BOOLEAN


def test_comparison_requires_integer_operands():
    for source in [
        "true < 10",
        "10 > true",
        "true == 10",
        "10 != true",
    ]:
        expression = Parser(
            Lexer(source).tokenize()
        ).parse_expression()

        try:
            SemanticAnalyzer()._analyze_expression(expression)
        except SemanticError:
            pass
        else:
            raise AssertionError(
                f"Expected SemanticError for: {source}"
            )


def test_boolean_expressions_return_boolean():
    for source in [
        "!true",
        "!false",
        "true && false",
        "true || false",
        "10 < 20 && 5 > 2",
        "10 < 20 || 5 > 2",
    ]:
        expression = Parser(
            Lexer(source).tokenize()
        ).parse_expression()

        result = SemanticAnalyzer()._analyze_expression(expression)

        assert result == BOOLEAN


def test_boolean_operators_require_boolean_operands():
    for source in [
        "!10",
        "10 && true",
        "true || 10",
    ]:
        expression = Parser(
            Lexer(source).tokenize()
        ).parse_expression()

        try:
            SemanticAnalyzer()._analyze_expression(expression)
        except SemanticError:
            pass
        else:
            raise AssertionError(
                f"Expected SemanticError for: {source}"
            )


def test_if_requires_boolean_condition():
    source = """if 10 {
    let x = 1
}"""

    program = Parser(
        Lexer(source).tokenize()
    ).parse_program()

    try:
        SemanticAnalyzer().analyze(program)
    except SemanticError as error:
        assert "If condition requires a boolean expression" in error.message
    else:
        raise AssertionError("Expected IF condition type error")


def test_while_requires_boolean_condition():
    source = """while 10 {
    let x = 1
}"""

    program = Parser(
        Lexer(source).tokenize()
    ).parse_program()

    try:
        SemanticAnalyzer().analyze(program)
    except SemanticError as error:
        assert "While condition requires a boolean expression" in error.message
    else:
        raise AssertionError("Expected WHILE condition type error")


def test_nested_control_flow_semantics():
    source = """while true {
    if false {
        let x = 1
    } else {
        let y = 2
    }
}"""

    program = Parser(
        Lexer(source).tokenize()
    ).parse_program()

    SemanticAnalyzer().analyze(program)


def test_nested_else_semantic_error():
    source = """while true {
    if false {
        let x = 1
    } else {
        let y = unknown_variable
    }
}"""

    program = Parser(
        Lexer(source).tokenize()
    ).parse_program()

    try:
        SemanticAnalyzer().analyze(program)
    except SemanticError:
        pass
    else:
        raise AssertionError(
            "Expected nested ELSE semantic error"
        )
