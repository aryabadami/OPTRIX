from errors import ParserError
from opx_ast.ast import Number, BinaryOp


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()

        if token.kind != "EOF":
            self.position += 1

        return token

    def expect(self, kind):
        token = self.current()

        if token.kind != kind:
            raise ParserError(
                f"Expected {kind}, got {token.kind}",
                line=1,
                column=self.position + 1,
            )

        self.advance()

        return token

    def parse_number(self):
        token = self.expect("NUMBER")

        return Number(
            int(token.value)
        )

    def parse_primary(self):
        token = self.current()

        if token.kind == "NUMBER":
            return self.parse_number()

        if token.kind == "LPAREN":
            self.advance()

            expression = self.parse_expression()

            self.expect("RPAREN")

            return expression

        raise ParserError(
            f"Unexpected token: {token.kind}",
            line=1,
            column=self.position + 1,
        )

    def parse_factor(self):
        left = self.parse_primary()

        while self.current().kind in {
            "STAR",
            "SLASH",
        }:
            operator = self.advance()

            right = self.parse_primary()

            left = BinaryOp(
                operator=operator.value,
                left=left,
                right=right,
            )

        return left

    def parse_expression(self):
        left = self.parse_factor()

        while self.current().kind in {
            "PLUS",
            "MINUS",
        }:
            operator = self.advance()

            right = self.parse_factor()

            left = BinaryOp(
                operator=operator.value,
                left=left,
                right=right,
            )

        return left

    def synchronize(self):
        """
        Recover from a parser error.

        Advance until a token is reached that can safely
        represent the beginning of another expression.
        """

        while self.current().kind != "EOF":

            if self.current().kind in {
                "NUMBER",
                "LPAREN",
            }:
                return

            self.advance()

    def parse(self):

        try:
            expression = self.parse_expression()

            self.expect("EOF")

            return expression

        except ParserError as error:

            self.errors.append(error)

            self.synchronize()

            return None


def parse(tokens):
    parser = Parser(tokens)

    result = parser.parse()

    if parser.errors:
        raise parser.errors[0]

    return result
