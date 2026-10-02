from ..ir.module import IRFunction
from .frame import ExecutionFrame


class ArgumentBindingError(RuntimeError):
    pass


class ArgumentBinder:

    def bind(
        self,
        function: IRFunction,
        arguments: list[object],
        frame: ExecutionFrame,
    ) -> None:

        parameters = function.parameters

        if len(arguments) != len(parameters):
            raise ArgumentBindingError(
                f"Function '{function.name}' expects "
                f"{len(parameters)} argument(s), "
                f"got {len(arguments)}"
            )

        for parameter, argument in zip(
            parameters,
            arguments,
        ):
            frame.set_variable(
                parameter,
                argument,
            )
