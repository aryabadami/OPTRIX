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
        source=None,
    ):
        super().__init__(message)

        self.message = message
        self.phase = phase
        self.line = line
        self.column = column
        self.source = source

    def format_context(self):
        if not self.source or self.line is None or self.column is None:
            return ""

        lines = self.source.splitlines()

        if self.line < 1 or self.line > len(lines):
            return ""

        source_line = lines[self.line - 1]

        caret_column = max(self.column - 1, 0)
        caret = " " * caret_column + "^"

        return f"{source_line}\n{caret}"

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
        source=None,
    ):
        super().__init__(
            message,
            phase="Parser",
            line=line,
            column=column,
            source=source,
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
