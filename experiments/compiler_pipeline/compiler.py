from pathlib import Path

from lexer.lexer import lex
from parser.parser import parse
from codegen.codegen import generate
from ir.executor import IRExecutor


def compile_source(source: str):

    print("=== SOURCE ===")
    print(source)

    # -------------------------
    # LEXER
    # -------------------------

    tokens = lex(source)

    print("\n=== TOKENS ===")

    for token in tokens:
        print(token)

    # -------------------------
    # PARSER
    # -------------------------

    tree = parse(tokens)

    print("\n=== AST ===")
    print(tree)

    # -------------------------
    # CODE GENERATION
    # -------------------------

    instructions = generate(tree)

    print("\n=== IR ===")

    for instruction in instructions:
        print(instruction)

    # -------------------------
    # EXECUTION
    # -------------------------

    executor = IRExecutor()

    result = executor.execute(
        instructions
    )

    print("\n=== RESULT ===")
    print(result)

    return result


def main():

    source_file = Path(
        "experiments/compiler_pipeline/source.opx"
    )

    source = source_file.read_text()

    compile_source(source)


if __name__ == "__main__":
    main()
