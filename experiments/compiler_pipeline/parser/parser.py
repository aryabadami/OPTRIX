from opx_ast.ast import Number, BinaryOp
from errors import ParserError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        token = self.current()
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

        return self.advance()

    def parse(self):
        expression = self.parse_expression()

        self.expect("EOF")

        return expression

    def parse_expression(self):
        left = self.parse_term()

        while self.current().kind in ("PLUS", "MINUS"):
            operator = self.advance()

            right = self.parse_term()

            left = BinaryOp(
                operator.value,
                left,
                right
            )

        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.current().kind in ("STAR", "SLASH"):
            operator = self.advance()

            right = self.parse_factor()

            left = BinaryOp(
                operator.value,
                left,
                right
            )

        return left

    def parse_factor(self):
        token = self.current()

        # Number
        if token.kind == "NUMBER":
            self.advance()

            return Number(
                int(token.value)
            )

        # Parenthesized expression
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


def parse(tokens):
    parser = Parser(tokens)

    return parser.parse()
