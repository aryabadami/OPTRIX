from ..ir.instructions import Call
from ..ir.module import IRModule
from .arguments import ArgumentBinder
from .call_stack import CallStack
from .frame import ExecutionFrame


class CallExecutionError(RuntimeError):
    pass


class CallExecutor:

    def __init__(self, module: IRModule) -> None:
        self.module = module
        self.stack = CallStack()
        self.binder = ArgumentBinder()

    def execute(
        self,
        call: Call,
        arguments: list[object],
        caller_frame: ExecutionFrame,
    ) -> ExecutionFrame:

        try:
            function = self.module.get_function(
                call.callee
            )
        except ValueError as error:
            raise CallExecutionError(
                str(error)
            ) from error

        callee_frame = ExecutionFrame(
            function,
            return_destination=call.result,
        )

        self.binder.bind(
            function,
            arguments,
            callee_frame,
        )

        self.stack.push(caller_frame)
        self.stack.push(callee_frame)

        return callee_frame
