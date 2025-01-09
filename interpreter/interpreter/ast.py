from .token import Token, TokenType

class Node:
    pass

class Number(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"{self.__class__.__name__} ({self.token})"

class Variable(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"{self.__class__.__name__} ({self.token})"

class Empty(Node):
    def __init__(self):
        self.token = ''

    def __str__(self):
        return f"{self.__class__.__name__} {self.token}"

class Assignment(Node):
    def __init__(self, var: Variable, op: Token, expr: Node):
        self.var = var
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"{self.__class__.__name__} ({self.var} {self.op} {self.expr})"

class Semicolon(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def __str__(self):
        return f"Semicolon ({self.left}, {self.right})"

class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"{self.__class__.__name__}" \
            f" {self.op.value} ({self.left}, {self.right})"

class UnaryOp(Node):
    def __init__(self, op: Token, expr: Node):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"{self.__class__.__name__} {self.op.value} ({self.expr})"