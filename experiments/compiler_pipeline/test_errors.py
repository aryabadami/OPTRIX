from errors import (
    CompilerError,
    LexerError,
    ParserError,
    SemanticError,
    CodegenError,
    IRVerificationError,
    RuntimeErrorOPX,
)


def test_base_error():
    error = CompilerError("something went wrong")

    assert error.message == "something went wrong"
    assert error.phase is None
    assert error.line is None
    assert error.column is None

    print("PASS: base compiler error")


def test_lexer_error():
    error = LexerError(
        "unexpected character",
        line=1,
        column=5,
    )

    assert error.phase == "Lexer"
    assert error.line == 1
    assert error.column == 5

    print("PASS: lexer error")


def test_parser_error():
    error = ParserError(
        "unexpected token",
        line=2,
        column=3,
    )

    assert error.phase == "Parser"
    assert error.line == 2
    assert error.column == 3

    print("PASS: parser error")


def test_semantic_error():
    error = SemanticError(
        "undefined variable"
    )

    assert error.phase == "Semantic"

    print("PASS: semantic error")


def test_codegen_error():
    error = CodegenError(
        "unsupported operation"
    )

    assert error.phase == "Codegen"

    print("PASS: codegen error")


def test_ir_verification_error():
    error = IRVerificationError(
        "invalid stack state"
    )

    assert error.phase == "IR Verification"

    print("PASS: IR verification error")


def test_runtime_error():
    error = RuntimeErrorOPX(
        "division by zero"
    )

    assert error.phase == "Runtime"

    print("PASS: runtime error")


def test_string_formatting():
    error = ParserError(
        "unexpected token",
        line=4,
        column=8,
    )

    expected = (
        "[Parser] unexpected token "
        "(line 4, column 8)"
    )

    assert str(error) == expected

    print("PASS: error formatting")


def main():
    print("=" * 60)
    print("OPTRIX ERROR INFRASTRUCTURE TESTS")
    print("=" * 60)

    test_base_error()
    test_lexer_error()
    test_parser_error()
    test_semantic_error()
    test_codegen_error()
    test_ir_verification_error()
    test_runtime_error()
    test_string_formatting()

    print()
    print("=" * 60)
    print("ALL ERROR TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
