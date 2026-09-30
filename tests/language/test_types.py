from language.optrix.semantic.types import (
    BOOLEAN,
    INTEGER,
    TypeKind,
)


def test_integer_type_exists():
    assert INTEGER.kind is TypeKind.INTEGER


def test_boolean_type_exists():
    assert BOOLEAN.kind is TypeKind.BOOLEAN


def test_integer_and_boolean_are_different():
    assert INTEGER != BOOLEAN


if __name__ == "__main__":
    test_integer_type_exists()
    test_boolean_type_exists()
    test_integer_and_boolean_are_different()

    print("PASS: type system tests")
