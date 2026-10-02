from language.optrix.ast import (
    BinaryExpression,
    Block,
    Identifier,
    IfStatement,
    IntegerLiteral,
    LetStatement,
    WhileStatement,
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


def test_arithmetic_operator_precedence():
    expression = parse_expression("10 + 2 * 3")

    assert expression.operator == "+"
    assert expression.left.value == 10

    assert expression.right.operator == "*"
    assert expression.right.left.value == 2
    assert expression.right.right.value == 3


def test_arithmetic_operators():
    for source, operator in [
        ("10 - 3", "-"),
        ("10 * 3", "*"),
        ("10 / 3", "/"),
    ]:
        expression = parse_expression(source)

        assert expression.operator == operator


def test_parse_if_statement():
    source = """if true {
    let x = 5
}"""

    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()

    assert len(program.statements) == 1

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert statement.condition.value is True

    assert isinstance(statement.then_branch, Block)
    assert len(statement.then_branch.statements) == 1

    inner = statement.then_branch.statements[0]

    assert isinstance(inner, LetStatement)
    assert inner.name == "x"
    assert inner.value.value == 5

    assert statement.else_branch is None


def test_parse_if_else_statement():
    source = """if true {
    let x = 1
} else {
    let x = 2
}"""

    program = Parser(
        Lexer(source).tokenize()
    ).parse_program()

    assert len(program.statements) == 1

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert isinstance(statement.then_branch, Block)
    assert isinstance(statement.else_branch, Block)

    then_stmt = statement.then_branch.statements[0]
    else_stmt = statement.else_branch.statements[0]

    assert isinstance(then_stmt, LetStatement)
    assert isinstance(else_stmt, LetStatement)

    assert then_stmt.name == "x"
    assert then_stmt.value.value == 1

    assert else_stmt.name == "x"
    assert else_stmt.value.value == 2


def test_parse_while_statement():
    source = """while true {
    let x = 5
}"""

    program = Parser(
        Lexer(source).tokenize()
    ).parse_program()

    assert len(program.statements) == 1

    statement = program.statements[0]

    assert isinstance(statement, WhileStatement)
    assert statement.condition.value is True

    assert isinstance(statement.body, Block)
    assert len(statement.body.statements) == 1

    inner = statement.body.statements[0]

    assert isinstance(inner, LetStatement)
    assert inner.name == "x"
    assert inner.value.value == 5


def test_parse_nested_while_if_else():
    source = """while true {
    if false {
        let x = 1
    } else {
        let x = 2
    }
}"""

    program = Parser(
        Lexer(source).tokenize()
    ).parse_program()

    assert len(program.statements) == 1

    outer = program.statements[0]

    assert isinstance(outer, WhileStatement)
    assert outer.condition.value is True
    assert isinstance(outer.body, Block)

    inner = outer.body.statements[0]

    assert isinstance(inner, IfStatement)
    assert inner.condition.value is False
    assert isinstance(inner.then_branch, Block)
    assert isinstance(inner.else_branch, Block)

    then_stmt = inner.then_branch.statements[0]
    else_stmt = inner.else_branch.statements[0]

    assert isinstance(then_stmt, LetStatement)
    assert isinstance(else_stmt, LetStatement)

    assert then_stmt.name == "x"
    assert then_stmt.value.value == 1

    assert else_stmt.name == "x"
    assert else_stmt.value.value == 2
