from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class IntegerLiteral:
    value: int


@dataclass(frozen=True)
class Identifier:
    name: str


@dataclass(frozen=True)
class BinaryExpression:
    left: "Expression"
    operator: str
    right: "Expression"


Expression = Union[
    IntegerLiteral,
    Identifier,
    BinaryExpression,
]


@dataclass(frozen=True)
class LetStatement:
    name: str
    value: Expression


@dataclass(frozen=True)
class Program:
    statements: list[LetStatement]
