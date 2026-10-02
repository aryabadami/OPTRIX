from opx_ast.ast import Number, BinaryOp

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

from errors.errors import CodegenError


def generate(expression):
    """
    Generate structured OPTRIX IR from an AST expression.

    AST
        ↓
    Module
        ↓
    Function
        ↓
    BasicBlock
        ↓
    Instructions
    """

    module = Module("optrix_module")

    function = Function("main")

    block = BasicBlock("entry")

    function.add_block(block)

    module.add_function(function)

    def emit(node):
        # --------------------------------------------------
        # Number
        # --------------------------------------------------

        if isinstance(node, Number):
            block.add_instruction(
                Push(node.value)
            )
            return

        # --------------------------------------------------
        # Binary operation
        # --------------------------------------------------

        if isinstance(node, BinaryOp):

            emit(node.left)

            emit(node.right)

            operator_map = {
                "+": Add,
                "-": Sub,
                "*": Mul,
                "/": Div,
            }

            instruction_class = operator_map.get(
                node.operator
            )

            if instruction_class is None:
                raise CodegenError(
                    f"Unsupported binary operator: "
                    f"{node.operator!r}"
                )

            block.add_instruction(
                instruction_class()
            )

            return

        # --------------------------------------------------
        # Unsupported AST node
        # --------------------------------------------------

        raise CodegenError(
            "Unsupported AST node: "
            f"{type(node).__name__}"
        )

    emit(expression)

    # Every generated function must terminate.
    block.add_instruction(
        Return()
    )

    return module
