from language.optrix.ast import BooleanLiteral


def test_boolean_literal():
    true_node = BooleanLiteral(True)
    false_node = BooleanLiteral(False)

    assert true_node.value is True
    assert false_node.value is False


if __name__ == "__main__":
    test_boolean_literal()

    print("PASS: AST tests")


def test_integer_literal_location():
    from language.optrix.source import SourceLocation

    location = SourceLocation(line=2, column=5)
    node = IntegerLiteral(10, location)

    assert node.value == 10
    assert node.location == location


def test_identifier_location():
    from language.optrix.ast import Identifier
    from language.optrix.source import SourceLocation

    location = SourceLocation(line=4, column=8)
    node = Identifier("answer", location)

    assert node.name == "answer"
    assert node.location == location
