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
                tokens.append(
                    self._single_character(TokenType.EQUAL)
                )
                continue

            if char == "+":
                tokens.append(
                    self._single_character(TokenType.PLUS)
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

        token_type = (
            TokenType.LET
            if lexeme == "let"
            else TokenType.IDENTIFIER
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
