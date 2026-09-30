from .ast import (
    BinaryExpression,
    Identifier,
    IntegerLiteral,
    LetStatement,
    Expression,
    Program,
)
from .tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse_expression(self) -> Expression:
        left = self._parse_primary()

        if self._current().type == TokenType.PLUS:
            operator = self._advance().lexeme
            right = self._parse_primary()

            return BinaryExpression(
                left=left,
                operator=operator,
                right=right,
            )

        return left

    def parse_program(self) -> Program:
        statements = []

        while self._current().type != TokenType.EOF:
            if self._current().type == TokenType.NEWLINE:
                self._advance()
                continue

            statements.append(self._parse_let_statement())

        return Program(statements)

    def _parse_let_statement(self) -> LetStatement:
        self._expect(TokenType.LET)

        name = self._expect(TokenType.IDENTIFIER)

        self._expect(TokenType.EQUAL)

        value = self.parse_expression()

        if self._current().type == TokenType.NEWLINE:
            self._advance()

        return LetStatement(
            name=name.lexeme,
            value=value,
        )

    def _parse_primary(self) -> Expression:
        token = self._current()

        if token.type == TokenType.INTEGER:
            self._advance()
            return IntegerLiteral(int(token.lexeme))

        if token.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(token.lexeme)

        raise SyntaxError(
            f"Expected expression at "
            f"{token.line}:{token.column}"
        )

    def _expect(self, token_type: TokenType) -> Token:
        token = self._current()

        if token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type.name}, "
                f"got {token.type.name} "
                f"at {token.line}:{token.column}"
            )

        return self._advance()

    def _current(self) -> Token:
        return self.tokens[self.position]

    def _advance(self) -> Token:
        token = self.tokens[self.position]
        self.position += 1
        return token
