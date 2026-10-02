from lexer.lexer import lex
from parser.parser import parse
from codegen.codegen import generate
from ir.executor import IRExecutor
from ir.printer import format_ir


def test_program(source, expected):
    print("=" * 60)
    print("SOURCE:", source)
    print("=" * 60)

    ast = parse(lex(source))
    module = generate(ast)

    print("IR:")
    print(format_ir(module))

    result = IRExecutor().execute(module)

    print("RESULT:", result)
    print("EXPECTED:", expected)

    if result != expected:
        raise AssertionError(
            f"{source}: got {result}, expected {expected}"
        )

    print("STATUS: PASS")
    print()


def main():
    tests = [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("5 * 6", 30),
        ("20 / 5", 4.0),
        ("(2 + 3) * 4", 20),
        ("2 + 3 * 4", 14),
        ("2 * 3 + 4", 10),
        ("10 - 2 - 3", 5),
        ("20 / 5 * 2", 8.0),
        ("2 + 3 * 4 - 5", 9),
    ]

    for source, expected in tests:
        test_program(source, expected)

    print("=" * 60)
    print("ALL IR TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
