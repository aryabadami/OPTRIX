from pipeline.compiler_pipeline import CompilerPipeline

from ir.ir import (
    Module,
    Function,
    BasicBlock,
    Push,
    Add,
    Return,
)

from ir.verifier import IRVerificationError


def make_invalid_ir():
    module = Module("invalid")

    function = Function("main")

    block = BasicBlock("entry")

    # Only one operand.
    # ADD requires two.
    block.add(Push(10))
    block.add(Add())
    block.add(Return())

    function.add_block(block)
    module.add_function(function)

    return module


def test_valid_pipeline():
    compiler = CompilerPipeline()

    result = compiler.compile(
        "2 + 3 * 4"
    )

    assert result == 14

    print(
        "PASS: valid pipeline "
        "verified and executed"
    )


def test_invalid_ir_blocked():
    compiler = CompilerPipeline()

    compiler.ir = make_invalid_ir()

    try:
        compiler.verify()

    except IRVerificationError:
        print(
            "PASS: invalid IR blocked "
            "before execution"
        )
        return

    raise AssertionError(
        "Invalid IR passed the verification gate"
    )


def main():
    print("=" * 60)
    print("OPTRIX PIPELINE VALIDATION GATE")
    print("=" * 60)

    test_valid_pipeline()

    test_invalid_ir_blocked()

    print()
    print("=" * 60)
    print("PIPELINE GATE TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
