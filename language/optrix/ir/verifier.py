from .instructions import (
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
from .module import IRFunction, IRModule


class IRVerificationError(Exception):
    pass


class IRVerifier:

    def verify(self, module: IRModule) -> None:
        for function in module.functions:
            self._verify_function(
                module,
                function,
            )

    def _verify_function(
        self,
        module: IRModule,
        function: IRFunction,
    ) -> None:
        labels = set()
        defined = set(function.parameters)

        for instruction in function.instructions:

            if isinstance(instruction, Label):
                if instruction.name in labels:
                    raise IRVerificationError(
                        f"Duplicate label: {instruction.name}"
                    )

                labels.add(instruction.name)

        for instruction in function.instructions:

            if isinstance(instruction, (ConstInt, ConstBool)):
                self._define(
                    instruction.result,
                    defined,
                )
                continue

            if isinstance(instruction, Load):
                self._define(
                    instruction.result,
                    defined,
                )
                continue

            if isinstance(instruction, Store):
                self._require(
                    instruction.value,
                    defined,
                )
                continue

            if isinstance(instruction, UnaryOp):
                self._require(
                    instruction.operand,
                    defined,
                )

                self._define(
                    instruction.result,
                    defined,
                )
                continue

            if isinstance(instruction, BinaryOp):
                self._require(
                    instruction.left,
                    defined,
                )

                self._require(
                    instruction.right,
                    defined,
                )

                self._define(
                    instruction.result,
                    defined,
                )
                continue

            if isinstance(instruction, Call):
                try:
                    callee = module.get_function(
                        instruction.callee
                    )
                except ValueError as error:
                    raise IRVerificationError(
                        str(error)
                    ) from error

                expected = len(callee.parameters)
                actual = len(instruction.arguments)

                if actual != expected:
                    raise IRVerificationError(
                        f"Argument count mismatch for "
                        f"{instruction.callee}: "
                        f"expected {expected}, "
                        f"got {actual}"
                    )

                for argument in instruction.arguments:
                    self._require(
                        argument,
                        defined,
                    )

                if instruction.result is not None:
                    self._define(
                        instruction.result,
                        defined,
                    )

                continue

            if isinstance(instruction, Jump):
                self._require_label(
                    instruction.target,
                    labels,
                )
                continue

            if isinstance(instruction, Branch):
                self._require(
                    instruction.condition,
                    defined,
                )

                self._require_label(
                    instruction.true_target,
                    labels,
                )

                self._require_label(
                    instruction.false_target,
                    labels,
                )
                continue

            if isinstance(instruction, Return):
                if instruction.value is not None:
                    self._require(
                        instruction.value,
                        defined,
                    )

                continue

            if isinstance(instruction, Label):
                continue

            raise IRVerificationError(
                f"Unknown instruction: "
                f"{type(instruction).__name__}"
            )

    @staticmethod
    def _define(
        name: str,
        defined: set[str],
    ) -> None:
        if not name:
            raise IRVerificationError(
                "Temporary name cannot be empty"
            )

        if name in defined:
            raise IRVerificationError(
                f"Temporary already defined: {name}"
            )

        defined.add(name)

    @staticmethod
    def _require(
        name: str,
        defined: set[str],
    ) -> None:
        if name not in defined:
            raise IRVerificationError(
                f"Use of undefined temporary: {name}"
            )

    @staticmethod
    def _require_label(
        name: str,
        labels: set[str],
    ) -> None:
        if name not in labels:
            raise IRVerificationError(
                f"Unknown label: {name}"
            )
