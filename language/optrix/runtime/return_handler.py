from .call_stack import CallStack
from .function_executor import FunctionReturn


class ReturnPropagationError(RuntimeError):
    pass


class ReturnHandler:

    def propagate(
        self,
        stack: CallStack,
        result: FunctionReturn,
    ) -> object | None:

        if stack.is_empty():
            raise ReturnPropagationError(
                "Cannot propagate return from empty call stack"
            )

        callee = stack.pop()

        if callee.return_destination is None:
            return result.value

        if stack.is_empty():
            raise ReturnPropagationError(
                "Callee has a return destination but no caller"
            )

        caller = stack.peek()

        caller.set_temporary(
            callee.return_destination,
            result.value,
        )

        return result.value
