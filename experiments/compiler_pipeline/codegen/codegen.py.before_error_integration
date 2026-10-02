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

from opx_ast.ast import Number, BinaryOp


def generate(expression):
    """
    Convert an OPTRIX AST into a structured OPTRIX IR module.

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

    def emit(node):

        # -------------------------
        # NUMBER
        # -------------------------

        if isinstance(node, Number):

            block.add_instruction(
                Push(node.value)
            )

            return

        # -------------------------
        # BINARY OPERATION
        # -------------------------

        if isinstance(node, BinaryOp):

            # Generate left side first
            emit(node.left)

            # Generate right side second
            emit(node.right)

            # Generate operation
            if node.operator == "+":

                block.add_instruction(
                    Add()
                )

            elif node.operator == "-":

                block.add_instruction(
                    Sub()
                )

            elif node.operator == "*":

                block.add_instruction(
                    Mul()
                )

            elif node.operator == "/":

                block.add_instruction(
                    Div()
                )

            else:

                raise ValueError(
                    f"Unsupported operator: {node.operator}"
                )

            return

        raise TypeError(
            f"Unsupported AST node: {type(node).__name__}"
        )

    # Generate expression instructions
    emit(expression)

    # Every expression currently returns its result
    block.add_instruction(
        Return()
    )

    module.add_function(function)

    return module
