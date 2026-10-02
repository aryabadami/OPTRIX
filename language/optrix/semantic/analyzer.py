from ..diagnostics import Diagnostic
from ..ast import (
    BinaryExpression,
    Block,
    BooleanLiteral,
    Identifier,
    IfStatement,
    IntegerLiteral,
    LetStatement,
    Program,
    UnaryExpression,
    WhileStatement,
)
from ..source import SourceLocation
from .symbols import SymbolTable
from .types import BOOLEAN, INTEGER


class SemanticError(Exception):
    def __init__(self, message: str, location: SourceLocation):
        super().__init__(message)
        self.message = message
        self.location = location

    def to_diagnostic(self) -> Diagnostic:
        return Diagnostic(
            message=self.message,
            location=self.location,
        )


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()

    def analyze(self, program: Program) -> None:
        for statement in program.statements:
            self._analyze_statement(statement)

    def _analyze_statement(self, statement) -> None:
        if isinstance(statement, LetStatement):
            value_type = self._analyze_expression(statement.value)
            self.symbols.define(statement.name, value_type)
            return

        if isinstance(statement, IfStatement):
            condition_type = self._analyze_expression(statement.condition)

            if condition_type != BOOLEAN:
                raise SemanticError(
                    "If condition requires a boolean expression",
                    statement.condition.location,
                )

            self._analyze_block(statement.then_branch)

            if statement.else_branch is not None:
                self._analyze_block(statement.else_branch)

            return

        if isinstance(statement, WhileStatement):
            condition_type = self._analyze_expression(statement.condition)

            if condition_type != BOOLEAN:
                raise SemanticError(
                    "While condition requires a boolean expression",
                    statement.condition.location,
                )

            self._analyze_block(statement.body)
            return

        raise SemanticError(
            f"Unknown statement: {type(statement).__name__}",
            getattr(statement, "location", None),
        )

    def _analyze_block(self, block: Block) -> None:
        for statement in block.statements:
            self._analyze_statement(statement)

    def _analyze_expression(self, expression):
        if isinstance(expression, IntegerLiteral):
            return INTEGER

        if isinstance(expression, BooleanLiteral):
            return BOOLEAN

        if isinstance(expression, Identifier):
            if not self.symbols.is_defined(expression.name):
                raise SemanticError(
                    f"Undefined variable: {expression.name}",
                    expression.location,
                )

            return self.symbols.get_type(expression.name)

        if isinstance(expression, UnaryExpression):
            operand_type = self._analyze_expression(expression.operand)

            if expression.operator == "!":
                if operand_type != BOOLEAN:
                    raise SemanticError(
                        "Operator '!' requires a boolean operand",
                        expression.operand.location,
                    )

                return BOOLEAN

            raise SemanticError(
                f"Unknown unary operator: {expression.operator}",
                expression.operand.location,
            )

        if isinstance(expression, BinaryExpression):
            left_type = self._analyze_expression(expression.left)
            right_type = self._analyze_expression(expression.right)

            if expression.operator in {"+", "-", "*", "/"}:
                if left_type != INTEGER or right_type != INTEGER:
                    raise SemanticError(
                        f"Operator '{expression.operator}' "
                        "requires integer operands",
                        expression.left.location,
                    )

                return INTEGER

            if expression.operator in {
                "<",
                ">",
                "==",
                "!=",
            }:
                if left_type != INTEGER or right_type != INTEGER:
                    raise SemanticError(
                        f"Operator '{expression.operator}' "
                        "requires integer operands",
                        expression.left.location,
                    )

                return BOOLEAN

            if expression.operator in {"&&", "||"}:
                if left_type != BOOLEAN or right_type != BOOLEAN:
                    raise SemanticError(
                        f"Operator '{expression.operator}' "
                        "requires boolean operands",
                        expression.left.location,
                    )

                return BOOLEAN

            raise SemanticError(
                f"Unknown binary operator: {expression.operator}",
                expression.left.location,
            )

        raise SemanticError(
            f"Unknown expression: {type(expression).__name__}",
            getattr(expression, "location", None),
        )
