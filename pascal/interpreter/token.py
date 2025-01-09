from enum import Enum, auto

class TokenType(Enum):
    BEGIN = auto()
    END = auto()

    NUMBER = auto()
    VARIABLE = auto()
    OPERATOR = auto()

    LPAREN = auto()
    RPAREN = auto()

    DOT = auto()
    SEMI = auto()
    ASSIGN = ()

    EOL = auto()

class Token:
    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.type_}, {self.value})"