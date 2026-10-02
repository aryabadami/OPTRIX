class Push:
    """
    Push a constant value onto the stack.
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Push({self.value!r})"


class Add:
    def __repr__(self):
        return "Add"


class Sub:
    def __repr__(self):
        return "Sub"


class Mul:
    def __repr__(self):
        return "Mul"


class Div:
    def __repr__(self):
        return "Div"


class Return:
    def __repr__(self):
        return "Return"


class BasicBlock:
    """
    Represents a basic block in OPTRIX IR.
    """

    def __init__(self, name):
        self.name = name
        self.instructions = []

    def add(self, instruction):
        self.instructions.append(instruction)

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def __repr__(self):
        return (
            f"BasicBlock("
            f"name={self.name!r}, "
            f"instructions={self.instructions!r}"
            f")"
        )


class Function:
    """
    Represents an OPTRIX IR function.
    """

    def __init__(self, name):
        self.name = name
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def __repr__(self):
        return (
            f"Function("
            f"name={self.name!r}, "
            f"blocks={self.blocks!r}"
            f")"
        )


class Module:
    """
    Top-level container for OPTRIX IR.
    """

    def __init__(self, name="main"):
        self.name = name
        self.functions = []

    def add_function(self, function):
        self.functions.append(function)

    def __repr__(self):
        return (
            f"Module("
            f"name={self.name!r}, "
            f"functions={self.functions!r}"
            f")"
        )
