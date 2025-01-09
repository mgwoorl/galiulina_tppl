from .token import Token, TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnaryOp, Variable, Assignment, Semicolon

class Parser():
    def __init__(self):
        self._lexer = Lexer()
        self._current_token = None

    def __check_token(self, type_: TokenType) -> None:
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()

        else:
            raise SyntaxError("invalid token order")

    def __factor(self):
        token = self._current_token
        if token.value == "+":
            self.__check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())

        if token.value == "-":
            self.__check_token(TokenType.OPERATOR)
            return UnaryOp(token, self.__factor())

        if token.type_ == TokenType.NUMBER:
            self.__check_token(TokenType.NUMBER)
            return Number(token)

        if token.type_ == TokenType.VARIABLE:
            self.__check_token(TokenType.VARIABLE)
            return Variable(token)

        if token.type_ == TokenType.LPAREN:
            self.__check_token(TokenType.LPAREN)
            result = self.__expr()
            self.__check_token(TokenType.RPAREN)
            return result
        raise SyntaxError("Invalid factor")

    # def program(self):
    #     result = self.complex_statement()
    #     self.__check_token(TokenType.DOT)
    #
    #     return result
    #
    # def complex_statement(self):
    #     result = []
    #     self.__check_token(TokenType.BEGIN)
    #     statements = self.statement_list()
    #     self.__check_token(TokenType.END)
    #
    #     for statement in statements:
    #         result.append(statement)
    #
    #     return result
    #
    # def statement_list(self):
    #     token = self._current_token
    #     node = self.statement()
    #
    #     results = [node]
    #
    #     while token.type_ == TokenType.SEMI:
    #         self.__check_token(TokenType.SEMI)
    #         results.append(self.statement())
    #
    #     if token.type_ == TokenType.VARIABLE:
    #         self.error()
    #
    #     return results
    #
    # def statement(self):
    #     token = self._current_token
    #     if token.type_ == TokenType.BEGIN:
    #         node = self.complex_statement()
    #     elif token.type_ == TokenType.VARIABLE:
    #         node = self.assignment_statement()
    #     else:
    #         node = self.empty()
    #     return node
    #
    # def assignment_statement(self):
    #     left = self._current_token
    #     self.__check_token(TokenType.VARIABLE)
    #     op = self._current_token
    #     self.__check_token(TokenType.ASSIGN)
    #     right = self.__expr()
    #     result = Assignment(left, op, right)
    #
    #     return result

    def __term(self) -> BinOp:
        result = self.__factor()
        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ["*", "/"]:
                break
            token = self._current_token
            self.__check_token(TokenType.OPERATOR)

            result = BinOp(result, token, self.__factor())
            # match token.value:
            #     case "*":
            #         result *= self.__factor()
            #
            #     case "/":
            #         result /= self.__factor()
            #
            #     case _:
            #         raise SyntaxError("term error")

        return result

    def __expr(self) -> BinOp:
        # self._lexer.init(s)
        # self._current_token = self._lexer.next()
        result = self.__term()

        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ["+", "-"]:
                break

            token = self._current_token
            self.__check_token(TokenType.OPERATOR)

            result = BinOp(result, token, self.__term())

        return result

    def __variable(self):
        token = self._current_token
        self.__check_token(TokenType.VARIABLE)
        return token

    def __assignment(self):
        left = self.__variable()
        op = self._current_token

        self.__check_token(TokenType.ASSIGN)

        right = self.__expr()
        return Assignment(left, op, right)

    def __empty(self):
        return None

    def __statement(self):
        if self._current_token.type_ == TokenType.BEGIN:
            return self.__complex_statement()
        if self._current_token.type_ == TokenType.VARIABLE:
            return self.__assignment()
        elif self._current_token.type_ == TokenType.END:
            return self.__empty()

        raise SyntaxError("Invalid statement")

    def __statement_list(self):
        result = self.__statement()
        if self._current_token and self._current_token.type_ == TokenType.SEMI:
            self._current_token = self._lexer.next()
            result = Semicolon(result, self.__statement_list())

        return result

    def __complex_statement(self):
        self.__check_token(TokenType.BEGIN)
        statements = self.__statement_list()
        self.__check_token(TokenType.END)

        return statements

    def __program(self) -> list:
        result = self.__complex_statement()
        self.__check_token(TokenType.DOT)

        return result

    def eval(self, s: str) -> list:
        self._lexer.init(s)
        self._current_token = self._lexer.next()
        return self.__program()

    # def eval(self, s: str) -> BinOp:
    #     self._lexer.init(s)
    #     self._current_token = self._lexer.next()
    #     return self.__expr()
