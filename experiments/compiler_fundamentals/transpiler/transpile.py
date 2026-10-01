import sys


def transpile(expression: str) -> str:
    return f"print({expression})"


def main():
    if len(sys.argv) != 2:
        print("usage: transpile.py '2 + 3'")
        raise SystemExit(1)

    print(transpile(sys.argv[1]))


if __name__ == "__main__":
    main()
