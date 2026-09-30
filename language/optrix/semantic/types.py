from enum import Enum, auto


class TypeKind(Enum):
    INTEGER = auto()
    BOOLEAN = auto()


class Type:
    def __init__(self, kind: TypeKind):
        self.kind = kind

    def __eq__(self, other):
        if not isinstance(other, Type):
            return NotImplemented

        return self.kind == other.kind

    def __repr__(self):
        return f"Type({self.kind.name})"


INTEGER = Type(TypeKind.INTEGER)
BOOLEAN = Type(TypeKind.BOOLEAN)
