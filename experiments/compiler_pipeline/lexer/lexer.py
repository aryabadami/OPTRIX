from dataclasses import dataclass

from errors import LexerError


@dataclass
class Token:
    kind: str
    value: str


def lex(source: str) -> list[Token]:
    tokens = []

    i = 0

    while i < len(source):
        char = source[i]

        # --------------------------------------------------
        # Whitespace
        # --------------------------------------------------

        if char.isspace():
            i += 1
            continue

        # --------------------------------------------------
        # Numbers
        # --------------------------------------------------

        if char.isdigit():
            start = i

            while i < len(source) and source[i].isdigit():
                i += 1

            tokens.append(
                Token(
                    "NUMBER",
                    source[start:i],
                )
            )

            continue

        # --------------------------------------------------
        # Plus
        # --------------------------------------------------

        if char == "+":
            tokens.append(
                Token("PLUS", char)
            )

            i += 1
            continue

        # --------------------------------------------------
        # Minus
        # --------------------------------------------------

        if char == "-":
            tokens.append(
                Token("MINUS", char)
            )

            i += 1
            continue

        # --------------------------------------------------
        # Multiplication
        # --------------------------------------------------

        if char == "*":
            tokens.append(
                Token("STAR", char)
            )

            i += 1
            continue

        # --------------------------------------------------
        # Division
        # --------------------------------------------------

        if char == "/":
            tokens.append(
                Token("SLASH", char)
            )

            i += 1
            continue

        # --------------------------------------------------
        # Left parenthesis
        # --------------------------------------------------

        if char == "(":
            tokens.append(
                Token("LPAREN", char)
            )

            i += 1
            continue

        # --------------------------------------------------
        # Right parenthesis
        # --------------------------------------------------

        if char == ")":
            tokens.append(
                Token("RPAREN", char)
            )

            i += 1
            continue

        # --------------------------------------------------
        # Unknown character
        # --------------------------------------------------

        raise LexerError(
            f"Unexpected character: {char!r}",
            line=1,
            column=i + 1,
        )

    # ------------------------------------------------------
    # End of file
    # ------------------------------------------------------

    tokens.append(
        Token("EOF", "")
    )

    return tokens
