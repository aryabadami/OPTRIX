from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    LET = auto()
    IDENTIFIER = auto()
    INTEGER = auto()

    EQUAL = auto()
    PLUS = auto()
    NEWLINE = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
