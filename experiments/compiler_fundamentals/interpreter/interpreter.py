import ast
import sys


def evaluate(expression: str):
    tree = ast.parse(expression, mode="eval")

    if not isinstance(tree.body, ast.BinOp):
        raise ValueError("Only arithmetic expressions are supported")

    if not isinstance(tree.body.left, ast.Constant):
        raise ValueError("Left operand must be an integer")

    if not isinstance(tree.body.right, ast.Constant):
        raise ValueError("Right operand must be an integer")

    left = tree.body.left.value
    right = tree.body.right.value

    if not isinstance(left, int) or not isinstance(right, int):
        raise ValueError("Operands must be integers")

    if isinstance(tree.body.op, ast.Add):
        return left + right

    if isinstance(tree.body.op, ast.Sub):
        return left - right

    if isinstance(tree.body.op, ast.Mult):
        return left * right

    raise ValueError("Unsupported operator")


def main():
    if len(sys.argv) != 2:
        print("usage: interpreter.py '2 + 3'")
        raise SystemExit(1)

    print(evaluate(sys.argv[1]))


if __name__ == "__main__":
    main()
