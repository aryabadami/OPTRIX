from dataclasses import dataclass

from lexer.lexer import Token


@dataclass
class Number:
    value: int


@dataclass
class BinaryOp:
    left: object
    operator: str
    right: object


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def current(self) -> Token:
        return self.tokens[self.position]

    def consume(self, kind: str) -> Token:
        token = self.current()

        if token.kind != kind:
            raise SyntaxError(
                f"Expected {kind}, got {token.kind}"
            )

        self.position += 1
        return token

    def parse_number(self):
        token = self.consume("NUMBER")

        return Number(
            int(token.value)
        )

    def parse_factor(self):
        """
        Parse multiplication and division.

        factor:
            NUMBER
            factor * NUMBER
            factor / NUMBER
        """

        left = self.parse_number()

        while self.current().kind in {
            "STAR",
            "SLASH",
        }:
            operator = self.current()

            self.position += 1

            right = self.parse_number()

            left = BinaryOp(
                left=left,
                operator=operator.value,
                right=right,
            )

        return left

    def parse_expression(self):
        """
        Parse addition and subtraction.

        expression:
            factor
            expression + factor
            expression - factor
        """

        left = self.parse_factor()

        while self.current().kind in {
            "PLUS",
            "MINUS",
        }:
            operator = self.current()

            self.position += 1

            right = self.parse_factor()

            left = BinaryOp(
                left=left,
                operator=operator.value,
                right=right,
            )

        return left

    def parse(self):
        expression = self.parse_expression()

        self.consume("EOF")

        return expression


def parse(tokens: list[Token]):
    parser = Parser(tokens)

    return parser.parse()
