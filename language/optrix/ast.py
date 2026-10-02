from dataclasses import dataclass
from typing import Union

from .source import SourceLocation


@dataclass(frozen=True)
class IntegerLiteral:
    value: int
    location: SourceLocation | None = None


@dataclass(frozen=True)
class BooleanLiteral:
    value: bool
    location: SourceLocation | None = None


@dataclass(frozen=True)
class Identifier:
    name: str
    location: SourceLocation | None = None


@dataclass(frozen=True)
class BinaryExpression:
    left: "Expression"
    operator: str
    right: "Expression"


@dataclass(frozen=True)
class UnaryExpression:
    operator: str
    operand: "Expression"


Expression = Union[
    IntegerLiteral,
    BooleanLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
]


@dataclass(frozen=True)
class LetStatement:
    name: str
    value: Expression


@dataclass(frozen=True)
class Block:
    statements: list["Statement"]


@dataclass(frozen=True)
class IfStatement:
    condition: Expression
    then_branch: Block
    else_branch: Block | None = None


@dataclass(frozen=True)
class WhileStatement:
    condition: Expression
    body: Block


Statement = Union[
    LetStatement,
    IfStatement,
    WhileStatement,
]


@dataclass(frozen=True)
class Program:
    statements: list["Statement"]
