from dataclasses import dataclass

from ..ir.instructions import (
    BinaryOp,
    Branch,
    Call,
    ConstBool,
    ConstInt,
    Jump,
    Label,
    Load,
    Return,
    Store,
    UnaryOp,
)
from ..ir.module import IRModule
from .arguments import ArgumentBinder
from .call_stack import CallStack
from .frame import ExecutionFrame


class FunctionExecutionError(RuntimeError):
    pass


@dataclass
class FunctionReturn:
    value: object | None


class FunctionExecutor:

    def __init__(
        self,
        module: IRModule | None = None,
        max_call_depth: int = 1024,
    ) -> None:

        if max_call_depth <= 0:
            raise ValueError(
                "max_call_depth must be positive"
            )

        self.module = module
        self.stack = CallStack()
        self.binder = ArgumentBinder()
        self.max_call_depth = max_call_depth

    def _resolve_operand(
        self,
        frame: ExecutionFrame,
        operand: str,
    ) -> object:
        if operand.startswith("%"):
            return frame.get_temporary(operand)

        return frame.get_variable(operand)

    def execute(
        self,
        frame: ExecutionFrame,
    ) -> FunctionReturn:

        self.stack.push(frame)

        try:
            return self._execute_frame(frame)
        finally:
            if not self.stack.is_empty():
                self.stack.pop()

    def _execute_frame(
        self,
        frame: ExecutionFrame,
    ) -> FunctionReturn:

        while frame.pc < len(
            frame.function.instructions
        ):

            instruction = frame.current_instruction()

            if isinstance(instruction, ConstInt):
                frame.set_temporary(
                    instruction.result,
                    instruction.value,
                )
                frame.advance()
                continue

            if isinstance(instruction, ConstBool):
                frame.set_temporary(
                    instruction.result,
                    instruction.value,
                )
                frame.advance()
                continue

            if isinstance(instruction, Load):
                value = frame.get_variable(
                    instruction.name
                )

                frame.set_temporary(
                    instruction.result,
                    value,
                )

                frame.advance()
                continue

            if isinstance(instruction, Store):
                value = self._resolve_operand(
                    frame,
                    instruction.value,
                )

                frame.set_variable(
                    instruction.name,
                    value,
                )

                frame.advance()
                continue

            if isinstance(instruction, UnaryOp):
                operand = self._resolve_operand(
                    frame,
                    instruction.operand,
                )

                result = self._execute_unary(
                    instruction.operator,
                    operand,
                )

                frame.set_temporary(
                    instruction.result,
                    result,
                )

                frame.advance()
                continue

            if isinstance(instruction, BinaryOp):
                left = self._resolve_operand(
                    frame,
                    instruction.left,
                )

                right = self._resolve_operand(
                    frame,
                    instruction.right,
                )

                result = self._execute_binary(
                    instruction.operator,
                    left,
                    right,
                )

                frame.set_temporary(
                    instruction.result,
                    result,
                )

                frame.advance()
                continue

            if isinstance(instruction, Jump):
                frame.pc = self._find_label(
                    frame,
                    instruction.target,
                )
                continue

            if isinstance(instruction, Branch):
                condition = self._resolve_operand(
                    frame,
                    instruction.condition,
                )

                target = (
                    instruction.true_target
                    if condition
                    else instruction.false_target
                )

                frame.pc = self._find_label(
                    frame,
                    target,
                )
                continue

            if isinstance(instruction, Label):
                frame.advance()
                continue

            if isinstance(instruction, Call):
                return self._execute_call(
                    frame,
                    instruction,
                )

            if isinstance(instruction, Return):
                value = None

                if instruction.value is not None:
                    value = self._resolve_operand(
                        frame,
                        instruction.value,
                    )

                return FunctionReturn(value)

            raise FunctionExecutionError(
                "Unsupported instruction during "
                f"function execution: "
                f"{type(instruction).__name__}"
            )

        return FunctionReturn(None)

    def _execute_call(
        self,
        caller: ExecutionFrame,
        instruction: Call,
    ) -> FunctionReturn:

        if self.module is None:
            raise FunctionExecutionError(
                "CALL requires an IRModule"
            )

        try:
            function = self.module.get_function(
                instruction.callee
            )
        except ValueError as error:
            raise FunctionExecutionError(
                str(error)
            ) from error

        arguments = [
            self._resolve_operand(caller, argument)
            for argument in instruction.arguments
        ]

        callee = ExecutionFrame(
            function,
            return_destination=instruction.result,
        )

        self.binder.bind(
            function,
            arguments,
            callee,
        )

        caller.advance()

        if self.stack.depth() >= self.max_call_depth:
            raise FunctionExecutionError(
                "Maximum call depth exceeded"
            )

        self.stack.push(callee)

        try:
            result = self._execute_frame(callee)
        finally:
            if not self.stack.is_empty():
                self.stack.pop()

        if instruction.result is not None:
            caller.set_temporary(
                instruction.result,
                result.value,
            )

        return self._continue_after_call(
            caller
        )

    def _continue_after_call(
        self,
        caller: ExecutionFrame,
    ) -> FunctionReturn:

        return self._execute_frame(
            caller
        )

    @staticmethod
    def _find_label(
        frame: ExecutionFrame,
        label: str,
    ) -> int:

        for index, instruction in enumerate(
            frame.function.instructions
        ):
            if isinstance(instruction, Label):
                if instruction.name == label:
                    return index

        raise FunctionExecutionError(
            f"Unknown label: {label}"
        )

    @staticmethod
    def _execute_unary(
        operator: str,
        operand: object,
    ) -> object:

        if operator == "NEG":
            return -operand

        if operator == "NOT":
            return not operand

        raise FunctionExecutionError(
            f"Unknown unary operator: {operator}"
        )

    @staticmethod
    def _execute_binary(
        operator: str,
        left: object,
        right: object,
    ) -> object:

        if operator == "ADD":
            return left + right

        if operator == "SUB":
            return left - right

        if operator == "MUL":
            return left * right

        if operator == "DIV":
            return left / right

        if operator == "MOD":
            return left % right

        if operator == "EQ":
            return left == right

        if operator == "NE":
            return left != right

        if operator == "LT":
            return left < right

        if operator == "LE":
            return left <= right

        if operator == "GT":
            return left > right

        if operator == "GE":
            return left >= right

        if operator == "AND":
            return left and right

        if operator == "OR":
            return left or right

        raise FunctionExecutionError(
            f"Unknown binary operator: {operator}"
        )
