from language.optrix.ast import (
    BinaryExpression,
    Identifier,
    IntegerLiteral,
)
from language.optrix.lexer import Lexer
from language.optrix.parser import Parser


def parse_expression(source):
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse_expression()


def test_parse_integer():
    node = parse_expression("42")

    assert isinstance(node, IntegerLiteral)
    assert node.value == 42


def test_parse_identifier():
    node = parse_expression("answer")

    assert isinstance(node, Identifier)
    assert node.name == "answer"


def test_parse_addition():
    node = parse_expression("a + b")

    assert isinstance(node, BinaryExpression)
    assert node.operator == "+"
    assert node.left.name == "a"
    assert node.right.name == "b"


def test_parse_let_statement():
    tokens = Lexer("let answer = 42").tokenize()
    program = Parser(tokens).parse_program()

    assert len(program.statements) == 1

    statement = program.statements[0]

    assert statement.name == "answer"
    assert isinstance(statement.value, IntegerLiteral)
    assert statement.value.value == 42


if __name__ == "__main__":
    test_parse_integer()
    test_parse_identifier()
    test_parse_addition()
    test_parse_let_statement()

    print("PASS: parser tests")


def test_parse_true():
    node = parse_expression("true")

    from language.optrix.ast import BooleanLiteral

    assert isinstance(node, BooleanLiteral)
    assert node.value is True


def test_parse_false():
    node = parse_expression("false")

    from language.optrix.ast import BooleanLiteral

    assert isinstance(node, BooleanLiteral)
    assert node.value is False


def test_integer_literal_preserves_source_location():
    node = parse_expression("42")

    from language.optrix.source import SourceLocation

    assert node.location == SourceLocation(line=1, column=1)


def test_identifier_preserves_source_location():
    node = parse_expression("answer")

    from language.optrix.source import SourceLocation

    assert node.location == SourceLocation(line=1, column=1)


def test_boolean_literal_preserves_source_location():
    true_node = parse_expression("true")
    false_node = parse_expression("false")

    from language.optrix.source import SourceLocation

    assert true_node.location == SourceLocation(line=1, column=1)
    assert false_node.location == SourceLocation(line=1, column=1)
