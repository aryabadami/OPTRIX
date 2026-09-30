from language.optrix.ast import (
    BinaryExpression,
    Identifier,
    IntegerLiteral,
    LetStatement,
    Program,
)


def test_integer_literal():
    node = IntegerLiteral(42)

    assert node.value == 42


def test_identifier():
    node = Identifier("answer")

    assert node.name == "answer"


def test_binary_expression():
    node = BinaryExpression(
        left=Identifier("a"),
        operator="+",
        right=IntegerLiteral(10),
    )

    assert node.left.name == "a"
    assert node.operator == "+"
    assert node.right.value == 10


def test_let_statement():
    node = LetStatement(
        name="answer",
        value=IntegerLiteral(42),
    )

    assert node.name == "answer"
    assert node.value.value == 42


def test_program():
    program = Program(
        statements=[
            LetStatement(
                name="answer",
                value=IntegerLiteral(42),
            )
        ]
    )

    assert len(program.statements) == 1
    assert program.statements[0].name == "answer"


if __name__ == "__main__":
    test_integer_literal()
    test_identifier()
    test_binary_expression()
    test_let_statement()
    test_program()

    print("PASS: AST tests")
