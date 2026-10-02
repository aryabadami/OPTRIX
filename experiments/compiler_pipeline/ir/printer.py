from ir.ir import (
    Module,
    Function,
    BasicBlock,
    Push,
    Add,
    Sub,
    Mul,
    Div,
    Return,
)


def print_instruction(instruction):
    if isinstance(instruction, Push):
        return f"push {instruction.value}"

    if isinstance(instruction, Add):
        return "add"

    if isinstance(instruction, Sub):
        return "sub"

    if isinstance(instruction, Mul):
        return "mul"

    if isinstance(instruction, Div):
        return "div"

    if isinstance(instruction, Return):
        return "return"

    raise TypeError(
        f"Unknown IR instruction: "
        f"{type(instruction).__name__}"
    )


def print_basic_block(block):
    lines = []

    lines.append(f"{block.name}:")

    for instruction in block.instructions:
        lines.append(
            f"    {print_instruction(instruction)}"
        )

    return "\n".join(lines)


def print_function(function):
    lines = []

    lines.append(
        f"fn @{function.name}() {{"
    )

    for block in function.blocks:
        lines.append("")
        lines.append(
            print_basic_block(block)
        )

    lines.append("}")

    return "\n".join(lines)


def print_module(module):
    lines = []

    lines.append(
        f"module @{module.name} {{"
    )

    for function in module.functions:
        lines.append("")
        lines.append(
            print_function(function)
        )

    lines.append("}")

    return "\n".join(lines)


def format_ir(module):
    return print_module(module)
