from dataclasses import dataclass, field

from ..ir.module import IRFunction


@dataclass
class ExecutionFrame:
    function: IRFunction
    pc: int = 0
    temporaries: dict[str, object] = field(default_factory=dict)
    variables: dict[str, object] = field(default_factory=dict)
    return_destination: str | None = None

    def get_temporary(self, name: str) -> object:
        if name not in self.temporaries:
            raise RuntimeError(
                f"Undefined temporary: {name}"
            )

        return self.temporaries[name]

    def set_temporary(
        self,
        name: str,
        value: object,
    ) -> None:
        self.temporaries[name] = value

    def get_variable(self, name: str) -> object:
        if name not in self.variables:
            raise RuntimeError(
                f"Undefined variable: {name}"
            )

        return self.variables[name]

    def set_variable(
        self,
        name: str,
        value: object,
    ) -> None:
        self.variables[name] = value

    def advance(self) -> None:
        self.pc += 1

    def current_instruction(self):
        if self.pc < 0:
            raise RuntimeError(
                f"Invalid program counter: {self.pc}"
            )

        if self.pc >= len(self.function.instructions):
            raise RuntimeError(
                f"Program counter out of range: {self.pc}"
            )

        return self.function.instructions[self.pc]
