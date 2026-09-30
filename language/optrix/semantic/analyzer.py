from ..ast import (
    BinaryExpression,
    Identifier,
    IntegerLiteral,
    Program,
)
from .symbols import SymbolTable


class SemanticError(Exception):
    pass


class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()

    def analyze(self, program: Program) -> None:
        for statement in program.statements:
            self._analyze_statement(statement)

    def _analyze_statement(self, statement) -> None:
        self._analyze_expression(statement.value)
        self.symbols.define(statement.name)

    def _analyze_expression(self, expression) -> None:
        if isinstance(expression, IntegerLiteral):
            return

        if isinstance(expression, Identifier):
            if not self.symbols.is_defined(expression.name):
                raise SemanticError(
                    f"Undefined variable: {expression.name}"
                )
            return

        if isinstance(expression, BinaryExpression):
            self._analyze_expression(expression.left)
            self._analyze_expression(expression.right)
            return

        raise SemanticError(
            f"Unknown expression: {type(expression).__name__}"
        )
