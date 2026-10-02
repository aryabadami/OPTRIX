from dataclasses import dataclass

from errors import LexerError


@dataclass
class Token:
    kind: str
    value: str
    line: int = 1
    column: int = 1


def lex(source: str) -> list[Token]:
    tokens = []

    i = 0
    line = 1
    column = 1

    while i < len(source):
        char = source[i]

        # Whitespace
        if char.isspace():
            if char == "\n":
                line += 1
                column = 1
            else:
                column += 1

            i += 1
            continue

        token_line = line
        token_column = column

        # Numbers
        if char.isdigit():
            start = i

            while i < len(source) and source[i].isdigit():
                i += 1
                column += 1

            tokens.append(
                Token(
                    "NUMBER",
                    source[start:i],
                    token_line,
                    token_column,
                )
            )

            continue

        # Plus
        if char == "+":
            tokens.append(
                Token(
                    "PLUS",
                    char,
                    token_line,
                    token_column,
                )
            )

            i += 1
            column += 1
            continue

        # Minus
        if char == "-":
            tokens.append(
                Token(
                    "MINUS",
                    char,
                    token_line,
                    token_column,
                )
            )

            i += 1
            column += 1
            continue

        # Multiplication
        if char == "*":
            tokens.append(
                Token(
                    "STAR",
                    char,
                    token_line,
                    token_column,
                )
            )

            i += 1
            column += 1
            continue

        # Division
        if char == "/":
            tokens.append(
                Token(
                    "SLASH",
                    char,
                    token_line,
                    token_column,
                )
            )

            i += 1
            column += 1
            continue

        # Left parenthesis
        if char == "(":
            tokens.append(
                Token(
                    "LPAREN",
                    char,
                    token_line,
                    token_column,
                )
            )

            i += 1
            column += 1
            continue

        # Right parenthesis
        if char == ")":
            tokens.append(
                Token(
                    "RPAREN",
                    char,
                    token_line,
                    token_column,
                )
            )

            i += 1
            column += 1
            continue

        raise LexerError(
            f"Unexpected character: {char!r}",
            line=token_line,
            column=token_column,
        )

    tokens.append(
        Token(
            "EOF",
            "",
            line,
            column,
        )
    )

    return tokens
