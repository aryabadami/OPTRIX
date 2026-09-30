from language.optrix.semantic.symbols import SymbolTable


def test_symbol_can_be_defined():
    symbols = SymbolTable()

    symbols.define("answer")

    assert symbols.is_defined("answer")


def test_unknown_symbol_is_not_defined():
    symbols = SymbolTable()

    assert not symbols.is_defined("answer")


if __name__ == "__main__":
    test_symbol_can_be_defined()
    test_unknown_symbol_is_not_defined()

    print("PASS: symbol table tests")
