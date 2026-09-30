from ..ast import (
    BinaryExpression,
    BooleanLiteral,
    Identifier,
    IntegerLiteral,
    Program,
)
from .symbols import SymbolTable
from .types import BOOLEAN, INTEGER


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()

    def analyze(self, program: Program) -> None:
        for statement in program.statements:
            self._analyze_statement(statement)

    def _analyze_statement(self, statement) -> None:
        value_type = self._analyze_expression(statement.value)
        self.symbols.define(statement.name, value_type)

    def _analyze_expression(self, expression):
        if isinstance(expression, IntegerLiteral):
            return INTEGER

        if isinstance(expression, BooleanLiteral):
            return BOOLEAN

        if isinstance(expression, Identifier):
            if not self.symbols.is_defined(expression.name):
                raise SemanticError(
                    f"Undefined variable: {expression.name}"
                )

            return self.symbols.get_type(expression.name)

        if isinstance(expression, BinaryExpression):
            left_type = self._analyze_expression(expression.left)
            right_type = self._analyze_expression(expression.right)

            if left_type != INTEGER or right_type != INTEGER:
                raise SemanticError(
                    "Operator '+' requires integer operands"
                )

            return INTEGER

        raise SemanticError(
            f"Unknown expression: {type(expression).__name__}"
        )
