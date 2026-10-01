class IRVerificationError(Exception):
    """Raised when OPTRIX IR is invalid."""


class IRVerifier:
    """
    Verifies OPTRIX IR structure, stack behaviour,
    operand types, and return correctness.
    """

    VALID_INSTRUCTIONS = {
        "Push",
        "Add",
        "Sub",
        "Mul",
        "Div",
        "Return",
    }

    SUPPORTED_VALUE_TYPES = (
        int,
        float,
    )

    def verify(self, module):
        self.verify_module(module)
        return True

    # ==================================================
    # MODULE
    # ==================================================

    def verify_module(self, module):
        if module is None:
            raise IRVerificationError(
                "Module cannot be None"
            )

        if not hasattr(module, "functions"):
            raise IRVerificationError(
                "Module is missing functions"
            )

        if not module.functions:
            raise IRVerificationError(
                "Module contains no functions"
            )

        for function in module.functions:
            self.verify_function(function)

    # ==================================================
    # FUNCTION
    # ==================================================

    def verify_function(self, function):
        if not getattr(function, "name", None):
            raise IRVerificationError(
                "Function is missing a name"
            )

        if not hasattr(function, "blocks"):
            raise IRVerificationError(
                f"Function '{function.name}' is missing blocks"
            )

        if not function.blocks:
            raise IRVerificationError(
                f"Function '{function.name}' contains no blocks"
            )

        for block in function.blocks:
            self.verify_block(function, block)

    # ==================================================
    # BLOCK
    # ==================================================

    def verify_block(self, function, block):
        if not getattr(block, "name", None):
            raise IRVerificationError(
                f"Function '{function.name}' contains "
                "a block without a name"
            )

        if not hasattr(block, "instructions"):
            raise IRVerificationError(
                f"Block '{block.name}' is missing instructions"
            )

        if not block.instructions:
            raise IRVerificationError(
                f"Block '{block.name}' contains no instructions"
            )

        stack = []
        terminated = False

        for index, instruction in enumerate(
            block.instructions
        ):
            instruction_name = type(instruction).__name__

            # ------------------------------------------
            # Nothing may appear after RETURN
            # ------------------------------------------

            if terminated:
                raise IRVerificationError(
                    f"Instruction '{instruction_name}' "
                    f"appears after Return in block "
                    f"'{block.name}'"
                )

            stack = self.verify_instruction(
                function,
                block,
                instruction,
                stack,
            )

            # ------------------------------------------
            # RETURN must terminate the block
            # ------------------------------------------

            if instruction_name == "Return":
                terminated = True

                if stack:
                    raise IRVerificationError(
                        f"Block '{block.name}' has "
                        f"{len(stack)} value(s) left "
                        "on the stack after Return"
                    )

        # ----------------------------------------------
        # Every block in the current execution model
        # must end with Return.
        # ----------------------------------------------

        if not terminated:
            raise IRVerificationError(
                f"Block '{block.name}' does not end "
                "with Return"
            )

    # ==================================================
    # INSTRUCTION
    # ==================================================

    def verify_instruction(
        self,
        function,
        block,
        instruction,
        stack,
    ):
        instruction_name = type(instruction).__name__

        if instruction_name not in self.VALID_INSTRUCTIONS:
            raise IRVerificationError(
                f"Unknown instruction "
                f"'{instruction_name}' "
                f"in block '{block.name}' "
                f"of function '{function.name}'"
            )

        # ----------------------------------------------
        # PUSH
        # ----------------------------------------------

        if instruction_name == "Push":

            if not hasattr(instruction, "value"):
                raise IRVerificationError(
                    "Push instruction is missing value"
                )

            value = instruction.value

            if isinstance(value, bool):
                raise IRVerificationError(
                    "Push does not support boolean values"
                )

            if not isinstance(
                value,
                self.SUPPORTED_VALUE_TYPES,
            ):
                raise IRVerificationError(
                    "Push value has unsupported type: "
                    f"{type(value).__name__}"
                )

            stack.append(type(value))

            return stack

        # ----------------------------------------------
        # BINARY OPERATIONS
        # ----------------------------------------------

        if instruction_name in {
            "Add",
            "Sub",
            "Mul",
            "Div",
        }:

            if len(stack) < 2:
                raise IRVerificationError(
                    f"{instruction_name} requires "
                    f"2 stack values, "
                    f"but only {len(stack)} available "
                    f"in block '{block.name}'"
                )

            right_type = stack.pop()
            left_type = stack.pop()

            valid_numeric_types = {
                int,
                float,
            }

            if (
                left_type not in valid_numeric_types
                or right_type not in valid_numeric_types
            ):
                raise IRVerificationError(
                    f"{instruction_name} requires "
                    "numeric operands"
                )

            if instruction_name == "Div":
                stack.append(float)

            elif float in {
                left_type,
                right_type,
            }:
                stack.append(float)

            else:
                stack.append(int)

            return stack

        # ----------------------------------------------
        # RETURN
        # ----------------------------------------------

        if instruction_name == "Return":

            if len(stack) != 1:
                raise IRVerificationError(
                    f"Return requires exactly "
                    f"1 stack value, "
                    f"but found {len(stack)} "
                    f"in block '{block.name}'"
                )

            stack.pop()

            return stack

        raise IRVerificationError(
            f"Unhandled instruction "
            f"'{instruction_name}'"
        )
