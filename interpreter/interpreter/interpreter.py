from .parser import Parser
from .ast import Number, BinOp, UnaryOp, Variable, Assignment, Semicolon, Empty

class NodeVisitor:
    def visit(self):
        pass

class Interpreter:
    def __init__(self):
        self._parser = Parser()

    def __visit_number(self, node: Number) -> float:
        return float(node.token.value)

    def __visit_binop(self, node: BinOp):
        match node.op.value:
            case "+":
                return self.visit(node.left) + self.visit(node.right)

            case "-":
                return self.visit(node.left) - self.visit(node.right)

            case "/":
                return self.visit(node.left) / self.visit(node.right)

            case "*":
                return self.visit(node.left) * self.visit(node.right)

            case "_":
                raise RuntimeError("Invalid operator")

    def __visit_unary(self, node):
        match node.op.value:
            case "+":
                return +self.visit(node.expr)

            case "-":
                return -self.visit(node.expr)

            case "_":
                raise RuntimeError("Bad unaryop")

    def __visit_variable(self, node):
        if node.token.value in self.value_variables.keys():
            return self.value_variables[node.token.value]

        raise ValueError(f"Uninitialized variable {node.token.value}")

    def __visit_assignment(self, node):
        var_name = node.var.value
        value = self.visit(node.expr)
        self.value_variables[var_name] = value

    def __visit_empty(self):
        return ''

    def __visit_semicolon(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit(self, node):
        if isinstance(node, Number):
            return self.__visit_number(node)

        elif isinstance(node, BinOp):
            return self.__visit_binop(node)

        elif isinstance(node, UnaryOp):
            return self.__visit_unary(node)

        elif isinstance(node, Empty):
            pass

        elif isinstance(node, Variable):
            return self.__visit_variable(node)

        elif isinstance(node, Assignment):
            return self.__visit_assignment(node)

        elif isinstance(node, Semicolon):
            return self.__visit_semicolon(node)

    def eval(self, code:str) -> float:
        self.value_variables = {}
        tree = self._parser.eval(code)
        self.visit(tree)

        return self.value_variables