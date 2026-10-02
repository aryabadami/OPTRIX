from dataclasses import dataclass, field

from .instructions import Instruction


@dataclass
class IRFunction:
    name: str
    parameters: list[str] = field(default_factory=list)
    instructions: list[Instruction] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.isidentifier():
            raise ValueError(
                f"Invalid function name: {self.name}"
            )

    def emit(self, instruction: Instruction) -> None:
        self.instructions.append(instruction)

    def add_parameter(self, name: str) -> None:
        if name in self.parameters:
            raise ValueError(
                f"Duplicate function parameter: {name}"
            )

        self.parameters.append(name)


@dataclass
class IRModule:
    functions: list[IRFunction] = field(default_factory=list)

    def add_function(self, function: IRFunction) -> None:
        if any(
            existing.name == function.name
            for existing in self.functions
        ):
            raise ValueError(
                f"Duplicate function: {function.name}"
            )

        self.functions.append(function)

    def get_function(self, name: str) -> IRFunction:
        for function in self.functions:
            if function.name == name:
                return function

        raise ValueError(
            f"Unknown function: {name}"
        )
