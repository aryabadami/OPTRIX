import ast
import sys


def compile_expression(expression: str) -> str:
    tree = ast.parse(expression, mode="eval")

    if not isinstance(tree.body, ast.BinOp):
        raise ValueError("Only binary expressions are supported")

    if not isinstance(tree.body.left, ast.Constant):
        raise ValueError("Left operand must be constant")

    if not isinstance(tree.body.right, ast.Constant):
        raise ValueError("Right operand must be constant")

    left = tree.body.left.value
    right = tree.body.right.value

    if isinstance(tree.body.op, ast.Add):
        operation = "ADD"
    elif isinstance(tree.body.op, ast.Sub):
        operation = "SUB"
    elif isinstance(tree.body.op, ast.Mult):
        operation = "MUL"
    else:
        raise ValueError("Unsupported operator")

    return f"PUSH {left}\nPUSH {right}\n{operation}"


def main():
    if len(sys.argv) != 2:
        print("usage: compiler.py '2 + 3'")
        raise SystemExit(1)

    print(compile_expression(sys.argv[1]))


if __name__ == "__main__":
    main()
