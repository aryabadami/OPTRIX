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

from ir.verifier import (
    IRVerifier,
    IRVerificationError,
)


def make_module(instructions):
    module = Module("test")
    function = Function("main")
    block = BasicBlock("entry")

    for instruction in instructions:
        block.add(instruction)

    function.add_block(block)
    module.add_function(function)

    return module


def expect_valid(name, instructions):
    module = make_module(instructions)

    try:
        IRVerifier().verify(module)
        print(f"PASS: {name}")
    except Exception as error:
        print(f"FAIL: {name}")
        print(f"      Unexpected error: {error}")
        raise


def expect_invalid(name, instructions):
    module = make_module(instructions)

    try:
        IRVerifier().verify(module)
    except IRVerificationError:
        print(f"PASS: {name}")
        return

    print(f"FAIL: {name}")
    print("      Invalid IR was accepted")
    raise AssertionError(
        f"Invalid IR was accepted: {name}"
    )


def test_valid_ir():
    expect_valid(
        "valid addition",
        [
            Push(2),
            Push(3),
            Add(),
            Return(),
        ],
    )

    expect_valid(
        "valid subtraction",
        [
            Push(10),
            Push(5),
            Sub(),
            Return(),
        ],
    )

    expect_valid(
        "valid multiplication",
        [
            Push(10),
            Push(5),
            Mul(),
            Return(),
        ],
    )

    expect_valid(
        "valid division",
        [
            Push(10),
            Push(5),
            Div(),
            Return(),
        ],
    )

    expect_valid(
        "valid floating point",
        [
            Push(10.5),
            Push(2.5),
            Add(),
            Return(),
        ],
    )

    expect_valid(
        "valid mixed numeric operands",
        [
            Push(10),
            Push(2.5),
            Add(),
            Return(),
        ],
    )


def test_invalid_stack_usage():
    expect_invalid(
        "binary operation with empty stack",
        [
            Add(),
            Return(),
        ],
    )

    expect_invalid(
        "binary operation with one operand",
        [
            Push(10),
            Add(),
            Return(),
        ],
    )

    expect_invalid(
        "subtraction with one operand",
        [
            Push(10),
            Sub(),
            Return(),
        ],
    )

    expect_invalid(
        "multiplication with one operand",
        [
            Push(10),
            Mul(),
            Return(),
        ],
    )

    expect_invalid(
        "division with one operand",
        [
            Push(10),
            Div(),
            Return(),
        ],
    )


def test_invalid_types():
    expect_invalid(
        "string operand rejected",
        [
            Push("hello"),
            Return(),
        ],
    )

    expect_invalid(
        "boolean operand rejected",
        [
            Push(True),
            Return(),
        ],
    )

    expect_invalid(
        "list operand rejected",
        [
            Push([1, 2, 3]),
            Return(),
        ],
    )

    expect_invalid(
        "object operand rejected",
        [
            Push(object()),
            Return(),
        ],
    )


def test_invalid_returns():
    expect_invalid(
        "return with empty stack",
        [
            Return(),
        ],
    )

    expect_invalid(
        "return with two values",
        [
            Push(10),
            Push(20),
            Return(),
        ],
    )

    expect_invalid(
        "return with three values",
        [
            Push(10),
            Push(20),
            Push(30),
            Return(),
        ],
    )

    expect_invalid(
        "instruction after return",
        [
            Push(10),
            Return(),
            Push(20),
        ],
    )

    expect_invalid(
        "missing return",
        [
            Push(10),
        ],
    )


def test_invalid_module():
    try:
        IRVerifier().verify(None)
    except IRVerificationError:
        print("PASS: invalid module rejected")
    else:
        raise AssertionError(
            "None module was accepted"
        )


def test_unknown_instruction():
    class UnknownInstruction:
        pass

    expect_invalid(
        "unknown instruction rejected",
        [
            Push(10),
            Push(20),
            UnknownInstruction(),
            Return(),
        ],
    )


def main():
    print("=" * 60)
    print("OPTRIX IR VERIFIER TEST SUITE")
    print("=" * 60)

    test_valid_ir()

    print()
    print("STACK VALIDATION")
    test_invalid_stack_usage()

    print()
    print("TYPE VALIDATION")
    test_invalid_types()

    print()
    print("RETURN VALIDATION")
    test_invalid_returns()

    print()
    print("MODULE VALIDATION")
    test_invalid_module()

    print()
    print("INSTRUCTION VALIDATION")
    test_unknown_instruction()

    print()
    print("=" * 60)
    print("ALL VERIFIER TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
