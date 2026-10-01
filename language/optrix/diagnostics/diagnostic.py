from dataclasses import dataclass
from enum import Enum, auto

from ..source import Source, SourceLocation


class DiagnosticSeverity(Enum):
    ERROR = auto()
    WARNING = auto()


@dataclass(frozen=True)
class Diagnostic:
    message: str
    location: SourceLocation
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR

    def format(
        self,
        source_name: str = "<source>",
        source: Source | None = None,
    ) -> str:
        severity = self.severity.name.lower()

        header = (
            f"{source_name}:{self.location.line}:"
            f"{self.location.column}: "
            f"{severity}: {self.message}"
        )

        if source is None:
            return header

        source_line = source.line(self.location.line)

        if not source_line:
            return header

        caret = " " * (self.location.column - 1) + "^"

        return f"{header}\n{source_line}\n{caret}"
