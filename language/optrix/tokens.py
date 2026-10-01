from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    LET = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    TRUE = auto()
    FALSE = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()

    AND_AND = auto()
    OR_OR = auto()
    NOT = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    NEWLINE = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int
