from dataclasses import dataclass


class Expr:
    pass


@dataclass
class Number(Expr):
    value: int


@dataclass
class Add(Expr):
    left: Expr
    right: Expr


@dataclass
class BinaryOp(Expr):
    operator: str
    left: Expr
    right: Expr
