class SymbolTable:
    def __init__(self):
        self._symbols = {}

    def define(self, name: str, type_info=None) -> None:
        self._symbols[name] = type_info

    def is_defined(self, name: str) -> bool:
        return name in self._symbols

    def get_type(self, name: str):
        return self._symbols[name]
