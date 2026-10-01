class CompilerError(Exception):
    """
    Base class for all OPTRIX compiler errors.
    """

    def __init__(
        self,
        message,
        phase=None,
        line=None,
        column=None,
    ):
        super().__init__(message)

        self.message = message
        self.phase = phase
        self.line = line
        self.column = column

    def __str__(self):
        parts = []

        if self.phase:
            parts.append(f"[{self.phase}]")

        parts.append(self.message)

        if self.line is not None:
            parts.append(
                f"(line {self.line}"
                + (
                    f", column {self.column}"
                    if self.column is not None
                    else ""
                )
                + ")"
            )

        return " ".join(parts)


class LexerError(CompilerError):
    """
    Error produced during lexical analysis.
    """

    def __init__(
        self,
        message,
        line=None,
        column=None,
    ):
        super().__init__(
            message,
            phase="Lexer",
            line=line,
            column=column,
        )


class ParserError(CompilerError):
    """
    Error produced during parsing.
    """

    def __init__(
        self,
        message,
        line=None,
        column=None,
    ):
        super().__init__(
            message,
            phase="Parser",
            line=line,
            column=column,
        )


class SemanticError(CompilerError):
    """
    Error produced during semantic analysis.
    """

    def __init__(
        self,
        message,
        line=None,
        column=None,
    ):
        super().__init__(
            message,
            phase="Semantic",
            line=line,
            column=column,
        )


class CodegenError(CompilerError):
    """
    Error produced during code generation.
    """

    def __init__(
        self,
        message,
        line=None,
        column=None,
    ):
        super().__init__(
            message,
            phase="Codegen",
            line=line,
            column=column,
        )


class IRVerificationError(CompilerError):
    """
    Error produced when generated IR is invalid.
    """

    def __init__(
        self,
        message,
        line=None,
        column=None,
    ):
        super().__init__(
            message,
            phase="IR Verification",
            line=line,
            column=column,
        )


class RuntimeErrorOPX(CompilerError):
    """
    Error produced during OPTRIX execution.
    """

    def __init__(
        self,
        message,
        line=None,
        column=None,
    ):
        super().__init__(
            message,
            phase="Runtime",
            line=line,
            column=column,
        )
