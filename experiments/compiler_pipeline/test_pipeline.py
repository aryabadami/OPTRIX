from pipeline.compiler_pipeline import CompilerPipeline


def test_program(compiler, source, expected):
    result = compiler.compile(source)

    assert result == expected, (
        f"{source}: expected {expected}, got {result}"
    )

    print(f"PASS: {source} = {result}")


def main():
    compiler = CompilerPipeline()

    tests = [
        ("2 + 3", 5),
        ("10 + 5", 15),
        ("10 - 5", 5),
        ("10 * 5", 50),
        ("10 / 5", 2.0),

        # Operator precedence
        ("2 + 3 * 4", 14),
        ("2 * 3 + 4", 10),
        ("10 - 2 - 3", 5),
        ("20 / 5 * 2", 8.0),
        ("2 + 3 * 4 - 5", 9),
    ]

    for source, expected in tests:
        test_program(
            compiler,
            source,
            expected,
        )

    print()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    main()
