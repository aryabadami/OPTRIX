from .ast import (
    BinaryExpression,
    UnaryExpression,
    Block,
    IfStatement,
    WhileStatement,
    Statement,
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
        return self._parse_logical_or()

    def _parse_logical_or(self) -> Expression:
        left = self._parse_logical_and()

        while self._current().type == TokenType.OR_OR:
            operator = self._advance().lexeme
            right = self._parse_logical_and()

            left = BinaryExpression(
                left=left,
                operator=operator,
                right=right,
            )

        return left

    def _parse_logical_and(self) -> Expression:
        left = self._parse_comparison()

        while self._current().type == TokenType.AND_AND:
            operator = self._advance().lexeme
            right = self._parse_comparison()

            left = BinaryExpression(
                left=left,
                operator=operator,
                right=right,
            )

        return left

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

            statements.append(self._parse_statement())

        return Program(statements)

    def _parse_statement(self) -> Statement:
        if self._current().type == TokenType.LET:
            return self._parse_let_statement()

        if self._current().type == TokenType.IF:
            return self._parse_if_statement()

        if self._current().type == TokenType.WHILE:
            return self._parse_while_statement()

        token = self._current()

        raise SyntaxError(
            f"Unexpected statement {token.type.name} "
            f"at {token.line}:{token.column}"
        )

    def _parse_while_statement(self) -> WhileStatement:
        self._expect(TokenType.WHILE)

        condition = self.parse_expression()
        body = self._parse_block()

        return WhileStatement(
            condition=condition,
            body=body,
        )


    def _parse_if_statement(self) -> IfStatement:
        self._expect(TokenType.IF)

        condition = self.parse_expression()
        then_branch = self._parse_block()

        else_branch = None

        if self._current().type == TokenType.ELSE:
            self._advance()
            else_branch = self._parse_block()

        return IfStatement(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch,
        )


    def _parse_block(self) -> Block:
        self._expect(TokenType.LEFT_BRACE)

        statements = []

        while self._current().type not in (
            TokenType.RIGHT_BRACE,
            TokenType.EOF,
        ):
            if self._current().type == TokenType.NEWLINE:
                self._advance()
                continue

            statements.append(self._parse_statement())

        self._expect(TokenType.RIGHT_BRACE)

        return Block(statements)


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

        if token.type == TokenType.NOT:
            self._advance()

            return UnaryExpression(
                operator="!",
                operand=self._parse_primary(),
            )

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
