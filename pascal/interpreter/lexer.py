from .token import Token, TokenType

class Lexer():
    def __init__(self):
        self._pos = 0
        self._text = ""
        self._current_char = None

    def __forward(self):
        self._pos += 1
        if self._pos > len(self._text) - 1:
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def __skip(self):
        while (self._current_char is not None and
               self._current_char.isspace()):
            self.__forward()

    def __integer(self):
        result = ""
        while (self._current_char is not None and self._current_char.isdigit() ):
            result += self._current_char
            self.__forward()
        return result

    def __number(self):
        result = ""
        decimal_found = False

        while (self._current_char is not None and (
                self._current_char.isdigit() or self._current_char == '.')):
            result += self._current_char
            self.__forward()

        return result

    def __id(self):
        result = ""

        while (self._current_char is not None and
               (self._current_char.isdigit() or self._current_char.isalpha() or self._current_char in "_")):
            result += self._current_char
            self.__forward()

        return result

    def init(self, s: str):
        self._text = s
        self._pos = 0
        self._current_char = self._text[self._pos]

    def next(self):
        while self._current_char:
            if self._current_char.isspace():
                self.__skip()
                continue
            if self._current_char.isalpha():
                ID = self.__id()
                if ID == "BEGIN":
                    return Token(TokenType.BEGIN, ID)
                elif ID == "END":
                    return Token(TokenType.END, ID)
                else:
                    return Token(TokenType.VARIABLE, ID)
            if self._current_char.isdigit():
                return Token(TokenType.NUMBER, self.__number())
            if self._current_char in ["+", "-", "*", "/"]:
                op = self._current_char
                self.__forward()
                return Token(TokenType.OPERATOR, op)
            if self._current_char == "(":
                val = self._current_char
                self.__forward()
                return Token(TokenType.LPAREN, val)
            if self._current_char == ")":
                val = self._current_char
                self.__forward()
                return Token(TokenType.RPAREN, val)
            if self._current_char == ".":
                val = self._current_char
                self.__forward()
                return Token(TokenType.DOT, val)
            if self._current_char == ":":
                val = ""
                val = self._current_char
                self.__forward()
                if self._current_char == "=":
                    val += self._current_char
                    self.__forward()
                    return Token(TokenType.ASSIGN, val)
            if self._current_char == ";":
                val = self._current_char
                self.__forward()
                return Token(TokenType.SEMI, val)
            else:
                raise SyntaxError("bad token")

        return Token(TokenType.EOL, "")