from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    pass


@dataclass(frozen=True)
class ConstInt(Instruction):
    result: str
    value: int


@dataclass(frozen=True)
class ConstBool(Instruction):
    result: str
    value: bool


@dataclass(frozen=True)
class Load(Instruction):
    result: str
    name: str


@dataclass(frozen=True)
class Store(Instruction):
    name: str
    value: str


@dataclass(frozen=True)
class BinaryOp(Instruction):
    result: str
    operator: str
    left: str
    right: str


@dataclass(frozen=True)
class UnaryOp(Instruction):
    result: str
    operator: str
    operand: str


@dataclass(frozen=True)
class Label(Instruction):
    name: str


@dataclass(frozen=True)
class Jump(Instruction):
    target: str


@dataclass(frozen=True)
class Branch(Instruction):
    condition: str
    true_target: str
    false_target: str


@dataclass(frozen=True)
class Return(Instruction):
    value: str | None = None


@dataclass(frozen=True)
class Call(Instruction):
    result: str | None
    callee: str
    arguments: list[str]
