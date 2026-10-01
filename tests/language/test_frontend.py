from pathlib import Path

from language.optrix.ast import BinaryExpression, IntegerLiteral
from language.optrix.lexer import Lexer
from language.optrix.parser import Parser


def test_hello_program():
    source = Path("examples/hello.opx").read_text()

    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()

    assert len(program.statements) == 3

    first = program.statements[0]
    assert first.name == "a"
    assert isinstance(first.value, IntegerLiteral)
    assert first.value.value == 10

    second = program.statements[1]
    assert second.name == "b"
    assert isinstance(second.value, IntegerLiteral)
    assert second.value.value == 20

    third = program.statements[2]
    assert third.name == "c"
    assert isinstance(third.value, BinaryExpression)
    assert third.value.operator == "+"
    assert third.value.left.name == "a"
    assert third.value.right.name == "b"


if __name__ == "__main__":
    test_hello_program()
    print("PASS: complete frontend test")


def test_arithmetic_program():
    source = """
let x = 10 + 2 * 3
let y = x - 4
let z = y / 2
"""

    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()

    assert len(program.statements) == 3

    x = program.statements[0]
    assert x.name == "x"
    assert isinstance(x.value, BinaryExpression)
    assert x.value.operator == "+"
    assert x.value.right.operator == "*"

    y = program.statements[1]
    assert y.name == "y"
    assert y.value.operator == "-"

    z = program.statements[2]
    assert z.name == "z"
    assert z.value.operator == "/"
