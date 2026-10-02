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

def test_codegen_error_propagation():
    from opx_ast.ast import Number, BinaryOp
    from codegen.codegen import generate
    from errors import CodegenError

    compiler_ast = BinaryOp(
        left=Number(2),
        operator="%",
        right=Number(3),
    )

    try:
        generate(compiler_ast)

    except CodegenError as error:
        print("PASS: codegen error propagation")
        print(f"PASS: propagated error = {error}")
        return

    raise AssertionError(
        "Expected CodegenError was not propagated"
    )

def test_parser_recovery():
    from lexer.lexer import lex
    from parser.parser import Parser

    tokens = lex("2 + + 3")

    parser = Parser(tokens)

    result = parser.parse()

    assert result is None
    assert len(parser.errors) == 1
    assert isinstance(parser.errors[0], ParserError)

    print("PASS: parser error recovery")


def test_parser_recovery_reaches_safe_token():
    from lexer.lexer import lex
    from parser.parser import Parser

    tokens = lex("2 + + 3")

    parser = Parser(tokens)

    parser.parse()

    assert parser.position < len(tokens)
    assert parser.current().kind == "NUMBER"

    print("PASS: parser recovery synchronization")


def test_parser_recovery_to_eof():
    from lexer.lexer import lex
    from parser.parser import Parser

    tokens = lex("2 +")

    parser = Parser(tokens)

    result = parser.parse()

    assert result is None
    assert len(parser.errors) == 1
    assert parser.current().kind == "EOF"

    print("PASS: parser recovery to EOF")

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
    test_codegen_error_propagation()

    test_parser_recovery()
    test_parser_recovery_reaches_safe_token()
    test_parser_recovery_to_eof()

    print()
    print("=" * 60)
    print("ALL ERROR TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()

