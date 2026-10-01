from dataclasses import dataclass


@dataclass(frozen=True)
class SourceLocation:
    line: int
    column: int


class Source:
    def __init__(self, text: str, name: str = "<source>"):
        self.text = text
        self.name = name

    def line(self, line_number: int) -> str:
        lines = self.text.splitlines()

        if line_number < 1 or line_number > len(lines):
            return ""

        return lines[line_number - 1]
