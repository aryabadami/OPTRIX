from language.optrix.diagnostics import (
    Diagnostic,
    DiagnosticSeverity,
)
from language.optrix.source import Source, SourceLocation


def test_error_diagnostic_format():
    diagnostic = Diagnostic(
        message="Undefined variable: a",
        location=SourceLocation(line=1, column=9),
    )

    assert diagnostic.format("example.opx") == (
        "example.opx:1:9: error: Undefined variable: a"
    )


def test_warning_diagnostic_format():
    diagnostic = Diagnostic(
        message="unused variable",
        location=SourceLocation(line=2, column=5),
        severity=DiagnosticSeverity.WARNING,
    )

    assert diagnostic.format("example.opx") == (
        "example.opx:2:5: warning: unused variable"
    )


if __name__ == "__main__":
    test_error_diagnostic_format()
    test_warning_diagnostic_format()

    print("PASS: diagnostic tests")


def test_error_diagnostic_includes_source_snippet():
    source = Source(
        "let b = a",
        "example.opx",
    )

    diagnostic = Diagnostic(
        message="Undefined variable: a",
        location=SourceLocation(line=1, column=9),
    )

    assert diagnostic.format(
        source_name="example.opx",
        source=source,
    ) == (
        "example.opx:1:9: error: Undefined variable: a\n"
        "let b = a\n"
        "        ^"
    )



def test_semantic_error_converts_to_diagnostic():
    from language.optrix.semantic.analyzer import SemanticError

    error = SemanticError(
        "Undefined variable: a",
        SourceLocation(line=1, column=9),
    )

    diagnostic = error.to_diagnostic()

    assert diagnostic.format("example.opx") == (
        "example.opx:1:9: error: Undefined variable: a"
    )
