import sys


def execute(program: str) -> int:
    stack = []

    for instruction in program.splitlines():
        parts = instruction.split()

        if parts[0] == "PUSH":
            stack.append(int(parts[1]))

        elif parts[0] == "ADD":
            right = stack.pop()
            left = stack.pop()
            stack.append(left + right)

        elif parts[0] == "SUB":
            right = stack.pop()
            left = stack.pop()
            stack.append(left - right)

        elif parts[0] == "MUL":
            right = stack.pop()
            left = stack.pop()
            stack.append(left * right)

        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    if len(stack) != 1:
        raise ValueError("Invalid program")

    return stack[0]


def main():
    program = sys.stdin.read()
    print(execute(program))


if __name__ == "__main__":
    main()
