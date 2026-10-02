from .instructions import (
    BinaryOp,
    Branch,
    ConstBool,
    ConstInt,
    Jump,
    Label,
    Load,
    Return,
    Store,
    UnaryOp,
)


class IRExecutionError(Exception):
    pass


class IRInterpreter:

    def __init__(self, max_steps=100000):
        self.temps = {}
        self.variables = {}
        self.max_steps = max_steps

    def execute(self, function):
        instructions = function.instructions

        labels = {
            instruction.name: index
            for index, instruction in enumerate(instructions)
            if isinstance(instruction, Label)
        }

        pc = 0
        steps = 0

        while pc < len(instructions):

            steps += 1

            if steps > self.max_steps:
                raise IRExecutionError(
                    "Execution exceeded maximum step limit"
                )

            instruction = instructions[pc]

            if isinstance(instruction, Label):
                pc += 1
                continue

            if isinstance(instruction, ConstInt):
                self.temps[instruction.result] = instruction.value
                pc += 1
                continue

            if isinstance(instruction, ConstBool):
                self.temps[instruction.result] = instruction.value
                pc += 1
                continue

            if isinstance(instruction, Load):
                if instruction.name not in self.variables:
                    raise IRExecutionError(
                        f"Undefined variable: {instruction.name}"
                    )

                self.temps[instruction.result] = (
                    self.variables[instruction.name]
                )

                pc += 1
                continue

            if isinstance(instruction, Store):
                if instruction.value not in self.temps:
                    raise IRExecutionError(
                        f"Undefined temporary: {instruction.value}"
                    )

                self.variables[instruction.name] = (
                    self.temps[instruction.value]
                )

                pc += 1
                continue

            if isinstance(instruction, UnaryOp):
                operand = self._value(
                    instruction.operand
                )

                self.temps[instruction.result] = (
                    self._unary(
                        instruction.operator,
                        operand,
                    )
                )

                pc += 1
                continue

            if isinstance(instruction, BinaryOp):
                left = self._value(
                    instruction.left
                )

                right = self._value(
                    instruction.right
                )

                self.temps[instruction.result] = (
                    self._binary(
                        instruction.operator,
                        left,
                        right,
                    )
                )

                pc += 1
                continue

            if isinstance(instruction, Branch):
                condition = self._value(
                    instruction.condition
                )

                target = (
                    instruction.true_target
                    if condition
                    else instruction.false_target
                )

                if target not in labels:
                    raise IRExecutionError(
                        f"Unknown label: {target}"
                    )

                pc = labels[target]
                continue

            if isinstance(instruction, Jump):
                if instruction.target not in labels:
                    raise IRExecutionError(
                        f"Unknown label: {instruction.target}"
                    )

                pc = labels[instruction.target]
                continue

            if isinstance(instruction, Return):
                if instruction.value is None:
                    return None

                return self._value(
                    instruction.value
                )

            raise IRExecutionError(
                f"Unsupported instruction: "
                f"{type(instruction).__name__}"
            )

        return self.variables

    def _value(self, operand):
        if operand not in self.temps:
            raise IRExecutionError(
                f"Undefined temporary: {operand}"
            )

        return self.temps[operand]

    def _unary(self, operator, operand):

        if operator == "-":
            return -operand

        if operator == "!":
            return not operand

        raise IRExecutionError(
            f"Unknown unary operator: {operator}"
        )

    def _binary(self, operator, left, right):

        if operator == "+":
            return left + right

        if operator == "-":
            return left - right

        if operator == "*":
            return left * right

        if operator == "/":
            return left / right

        if operator == "%":
            return left % right

        if operator == "==":
            return left == right

        if operator == "!=":
            return left != right

        if operator == "<":
            return left < right

        if operator == "<=":
            return left <= right

        if operator == ">":
            return left > right

        if operator == ">=":
            return left >= right

        if operator == "&&":
            return left and right

        if operator == "||":
            return left or right

        raise IRExecutionError(
            f"Unknown binary operator: {operator}"
        )
