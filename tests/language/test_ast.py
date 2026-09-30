from language.optrix.ast import BooleanLiteral


def test_boolean_literal():
    true_node = BooleanLiteral(True)
    false_node = BooleanLiteral(False)

    assert true_node.value is True
    assert false_node.value is False


if __name__ == "__main__":
    test_boolean_literal()

    print("PASS: AST tests")
