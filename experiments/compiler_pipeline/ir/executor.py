class IRExecutor:
    """
    Executes the structured OPTRIX IR.

    Expected structure:

    Module
      └── Function
            └── BasicBlock
                  └── Instructions
    """

    def __init__(self):
        self.stack = []

    def execute(self, module):
        """
        Execute an OPTRIX IR Module.

        Returns the final value produced by the Return instruction.
        """

        if not hasattr(module, "functions"):
            raise TypeError(
                "IRExecutor.execute() expected a Module object"
            )

        if not module.functions:
            raise ValueError(
                "IR module contains no functions"
            )

        # For this experimental compiler pipeline,
        # execute the main function.
        main_function = None

        for function in module.functions:
            if function.name == "main":
                main_function = function
                break

        if main_function is None:
            raise ValueError(
                "IR module does not contain a 'main' function"
            )

        self.stack = []

        return self._execute_function(main_function)

    def _execute_function(self, function):
        """
        Execute all basic blocks in a function.
        """

        if not function.blocks:
            raise ValueError(
                f"Function '{function.name}' contains no basic blocks"
            )

        for block in function.blocks:
            result = self._execute_block(block)

            # A Return instruction produces the final result.
            if result is not None:
                return result

        return None

    def _execute_block(self, block):
        """
        Execute every instruction inside one basic block.
        """

        instructions = block.instructions

        for instruction in instructions:

            instruction_name = type(instruction).__name__

            # PUSH
            if instruction_name == "Push":
                self.stack.append(instruction.value)

            # ADD
            elif instruction_name == "Add":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left + right)

            # SUB
            elif instruction_name == "Sub":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left - right)

            # MUL
            elif instruction_name == "Mul":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left * right)

            # DIV
            elif instruction_name == "Div":
                right = self.stack.pop()
                left = self.stack.pop()

                if right == 0:
                    raise ZeroDivisionError(
                        "division by zero"
                    )

                self.stack.append(left / right)

            # RETURN
            elif instruction_name == "Return":
                if not self.stack:
                    return None

                return self.stack.pop()

            else:
                raise ValueError(
                    f"Unsupported IR instruction: "
                    f"{instruction_name}"
                )

        return None


def execute(module):
    """
    Backwards-compatible helper.

    Allows:

        execute(module)

    as well as:

        IRExecutor().execute(module)
    """

    executor = IRExecutor()

    return executor.execute(module)
