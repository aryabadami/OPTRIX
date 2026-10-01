from .ast import (
    BinaryExpression,
    BooleanLiteral,
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
        return self._parse_comparison()

    def _parse_comparison(self) -> Expression:
        left = self._parse_additive()

        while self._current().type in (
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
        ):
            operator = self._advance().lexeme
            right = self._parse_additive()

            left = BinaryExpression(
                left=left,
                operator=operator,
                right=right,
            )

        return left

    def _parse_additive(self) -> Expression:
        left = self._parse_multiplicative()

        while self._current().type in (
            TokenType.PLUS,
            TokenType.MINUS,
        ):
            operator = self._advance().lexeme
            right = self._parse_multiplicative()

            left = BinaryExpression(
                left=left,
                operator=operator,
                right=right,
            )

        return left

    def _parse_multiplicative(self) -> Expression:
        left = self._parse_primary()

        while self._current().type in (
            TokenType.STAR,
            TokenType.SLASH,
        ):
            operator = self._advance().lexeme
            right = self._parse_primary()

            left = BinaryExpression(
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
            from .source import SourceLocation

            return IntegerLiteral(
                int(token.lexeme),
                SourceLocation(token.line, token.column),
            )

        if token.type == TokenType.TRUE:
            self._advance()
            from .source import SourceLocation

            return BooleanLiteral(
                True,
                SourceLocation(token.line, token.column),
            )

        if token.type == TokenType.FALSE:
            self._advance()
            from .source import SourceLocation

            return BooleanLiteral(
                False,
                SourceLocation(token.line, token.column),
            )

        if token.type == TokenType.IDENTIFIER:
            self._advance()
            from .source import SourceLocation

            return Identifier(
                token.lexeme,
                SourceLocation(token.line, token.column),
            )

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
