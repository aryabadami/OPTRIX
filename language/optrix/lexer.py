from .tokens import Token, TokenType


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens = []

        while self.position < len(self.source):
            char = self.source[self.position]

            if char in " \t":
                self._advance()
                continue

            if char == "\n":
                tokens.append(
                    Token(
                        TokenType.NEWLINE,
                        "\\n",
                        self.line,
                        self.column,
                    )
                )
                self._advance_line()
                continue

            if char.isalpha() or char == "_":
                tokens.append(self._identifier())
                continue

            if char.isdigit():
                tokens.append(self._integer())
                continue

            if char == "=":
                line = self.line
                column = self.column

                if (
                    self.position + 1 < len(self.source)
                    and self.source[self.position + 1] == "="
                ):
                    self._advance()
                    self._advance()
                    tokens.append(
                        Token(
                            TokenType.EQUAL_EQUAL,
                            "==",
                            line,
                            column,
                        )
                    )
                else:
                    tokens.append(
                        self._single_character(TokenType.EQUAL)
                    )

                continue

            if char == "!":
                line = self.line
                column = self.column

                if (
                    self.position + 1 < len(self.source)
                    and self.source[self.position + 1] == "="
                ):
                    self._advance()
                    self._advance()
                    tokens.append(
                        Token(
                            TokenType.NOT_EQUAL,
                            "!=",
                            line,
                            column,
                        )
                    )
                else:
                    tokens.append(
                        self._single_character(TokenType.NOT)
                    )

                continue

            if char == "&":
                line = self.line
                column = self.column

                if (
                    self.position + 1 < len(self.source)
                    and self.source[self.position + 1] == "&"
                ):
                    self._advance()
                    self._advance()
                    tokens.append(
                        Token(
                            TokenType.AND_AND,
                            "&&",
                            line,
                            column,
                        )
                    )
                else:
                    raise SyntaxError(
                        f"Unexpected character '&' at "
                        f"{line}:{column}"
                    )

                continue

            if char == "|":
                line = self.line
                column = self.column

                if (
                    self.position + 1 < len(self.source)
                    and self.source[self.position + 1] == "|"
                ):
                    self._advance()
                    self._advance()
                    tokens.append(
                        Token(
                            TokenType.OR_OR,
                            "||",
                            line,
                            column,
                        )
                    )
                else:
                    raise SyntaxError(
                        f"Unexpected character '|' at "
                        f"{line}:{column}"
                    )

                continue

            if char == "<":
                tokens.append(
                    self._single_character(TokenType.LESS)
                )
                continue

            if char == ">":
                tokens.append(
                    self._single_character(TokenType.GREATER)
                )
                continue

            if char == "+":
                tokens.append(
                    self._single_character(TokenType.PLUS)
                )
                continue

            if char == "-":
                tokens.append(
                    self._single_character(TokenType.MINUS)
                )
                continue

            if char == "*":
                tokens.append(
                    self._single_character(TokenType.STAR)
                )
                continue

            if char == "/":
                tokens.append(
                    self._single_character(TokenType.SLASH)
                )
                continue

            raise SyntaxError(
                f"Unexpected character '{char}' "
                f"at {self.line}:{self.column}"
            )

        tokens.append(
            Token(TokenType.EOF, "", self.line, self.column)
        )

        return tokens

    def _identifier(self) -> Token:
        start = self.position
        line = self.line
        column = self.column

        while (
            self.position < len(self.source)
            and (
                self.source[self.position].isalnum()
                or self.source[self.position] == "_"
            )
        ):
            self._advance()

        lexeme = self.source[start:self.position]

        keywords = {
            "let": TokenType.LET,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
        }

        token_type = keywords.get(
            lexeme,
            TokenType.IDENTIFIER,
        )

        return Token(token_type, lexeme, line, column)

    def _integer(self) -> Token:
        start = self.position
        line = self.line
        column = self.column

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            self._advance()

        return Token(
            TokenType.INTEGER,
            self.source[start:self.position],
            line,
            column,
        )

    def _single_character(self, token_type: TokenType) -> Token:
        line = self.line
        column = self.column
        lexeme = self.source[self.position]

        self._advance()

        return Token(token_type, lexeme, line, column)

    def _advance(self):
        self.position += 1
        self.column += 1

    def _advance_line(self):
        self.position += 1
        self.line += 1
        self.column = 1
