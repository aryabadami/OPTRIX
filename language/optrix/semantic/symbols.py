class SymbolTable:
    def __init__(self):
        self._symbols = set()

    def define(self, name: str) -> None:
        self._symbols.add(name)

    def is_defined(self, name: str) -> bool:
        return name in self._symbols
