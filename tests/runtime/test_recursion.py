from language.optrix.ir import (
    BinaryOp,
    Branch,
    Call,
    ConstInt,
    IRFunction,
    IRModule,
    Label,
    Load,
    Return,
)

from language.optrix.runtime import (
    ExecutionFrame,
    FunctionExecutor,
)


def build_factorial():
    factorial = IRFunction(
        "factorial",
        parameters=["n"],
    )

    factorial.emit(
        Load("%0", "n")
    )

    factorial.emit(
        ConstInt("%1", 1)
    )

    factorial.emit(
        BinaryOp(
            result="%2",
            operator="LE",
            left="%0",
            right="%1",
        )
    )

    factorial.emit(
        Branch(
            condition="%2",
            true_target="base",
            false_target="recursive",
        )
    )

    factorial.emit(
        Label("base")
    )

    factorial.emit(
        ConstInt("%3", 1)
    )

    factorial.emit(
        Return("%3")
    )

    factorial.emit(
        Label("recursive")
    )

    factorial.emit(
        ConstInt("%4", 1)
    )

    factorial.emit(
        BinaryOp(
            result="%5",
            operator="SUB",
            left="%0",
            right="%4",
        )
    )

    factorial.emit(
        Call(
            result="%6",
            callee="factorial",
            arguments=["%5"],
        )
    )

    factorial.emit(
        BinaryOp(
            result="%7",
            operator="MUL",
            left="%0",
            right="%6",
        )
    )

    factorial.emit(
        Return("%7")
    )

    return factorial


def run_factorial(n):
    factorial = build_factorial()

    main = IRFunction("main")

    main.emit(
        ConstInt("%0", n)
    )

    main.emit(
        Call(
            result="%1",
            callee="factorial",
            arguments=["%0"],
        )
    )

    main.emit(
        Return("%1")
    )

    module = IRModule()

    module.add_function(factorial)
    module.add_function(main)

    executor = FunctionExecutor(module)

    result = executor.execute(
        ExecutionFrame(main)
    )

    return result.value


def test_factorial_base_case():
    assert run_factorial(0) == 1
    assert run_factorial(1) == 1


def test_factorial_recursive_execution():
    assert run_factorial(2) == 2
    assert run_factorial(3) == 6
    assert run_factorial(4) == 24


def test_factorial_recursive_return_chain():
    assert run_factorial(5) == 120


def test_factorial_larger_input():
    assert run_factorial(6) == 720
