from lexer.lexer import lex
from parser.parser import parse
from codegen.codegen import generate

from ir.verifier import IRVerifier
from ir.executor import IRExecutor


class CompilerPipeline:
    """
    Complete OPTRIX compiler pipeline.

    SOURCE
        ↓
    LEXER
        ↓
    PARSER
        ↓
    AST
        ↓
    CODE GENERATION
        ↓
    IR
        ↓
    VERIFIER
        ↓
    EXECUTOR
        ↓
    RESULT
    """

    def __init__(self):
        self.source = None
        self.tokens = None
        self.ast = None
        self.ir = None
        self.result = None

        self.verifier = IRVerifier()
        self.executor = IRExecutor()

    # ==================================================
    # COMPILE
    # ==================================================

    def compile(self, source):
        self.source = source

        # ----------------------------------------------
        # 1. LEX
        # ----------------------------------------------

        self.tokens = lex(source)

        # ----------------------------------------------
        # 2. PARSE
        # ----------------------------------------------

        self.ast = parse(self.tokens, self.source)

        # ----------------------------------------------
        # 3. CODE GENERATION
        # ----------------------------------------------

        self.ir = generate(self.ast)

        # ----------------------------------------------
        # 4. VERIFICATION GATE
        # ----------------------------------------------

        self.verify()

        # ----------------------------------------------
        # 5. EXECUTION
        # ----------------------------------------------

        self.execute()

        return self.result

    # ==================================================
    # VERIFY
    # ==================================================

    def verify(self):
        """
        Verify generated IR before execution.

        Execution is not allowed unless verification
        succeeds.
        """

        if self.ir is None:
            raise RuntimeError(
                "Cannot verify: IR has not been generated"
            )

        self.verifier.verify(self.ir)

        return True

    # ==================================================
    # EXECUTE
    # ==================================================

    def execute(self):
        """
        Execute only verified IR.
        """

        if self.ir is None:
            raise RuntimeError(
                "Cannot execute: IR has not been generated"
            )

        self.result = self.executor.execute(
            self.ir
        )

        return self.result
