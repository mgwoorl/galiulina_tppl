import pytest
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter

@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()

class TestInterpreter:
    def test_add(self, interpreter):
        assert interpreter.eval("BEGIN x := 2+2; END.") == {'x': 4.0}
        assert interpreter.eval("BEGIN x := 2+3; END.") == {'x': 5.0}
        assert interpreter.eval("BEGIN x := 1+2+3; END.") == {'x': 6.0}

    def test_sub(self, interpreter):
        assert interpreter.eval("BEGIN x := 2-2; END.") == {'x': 0.0}
        assert interpreter.eval("BEGIN x := 2-3; END.") == {'x': -1.0}

    def test_spaces(self, interpreter):
        assert interpreter.eval("BEGIN x :=      2    -      2     ; END.") == {'x': 0.0}

    def test_int(self, interpreter):
        assert interpreter.eval("BEGIN x := 222 + 100000; END.") == {'x': 100222.0}

    def test_float(self, interpreter):
        assert interpreter.eval("BEGIN x := 22.2 + 10.0; END.") == {'x': 32.2}

    def test_term(self, interpreter):
       assert interpreter.eval("BEGIN x := 2+2+2; END.") == {'x': 6.0}

    def test_que(self, interpreter):
        assert interpreter.eval("BEGIN x := 2+2*2; END.") == {'x': 6.0}

    def test_parens(self, interpreter):
        assert interpreter.eval("BEGIN x := (2+2)*2; END.") == {'x': 8.0}

    def test_parent(self, interpreter):
        assert interpreter.eval("BEGIN x := (2+2)*2; END.") == {'x': 8.0}
        assert interpreter.eval("BEGIN x := ((((   2    )))); END.") == {'x': 2.0}
        assert interpreter.eval("BEGIN x := 2 + (2 * (3 + 5)); END.") == {'x': 18.0}

    def test_unary(self, interpreter):
       assert interpreter.eval("BEGIN x_ := -2; END.") == {'x': -2.0}
       assert interpreter.eval("BEGIN x := +2; END.") == {'x': 2.0}
       assert interpreter.eval("BEGIN x := -(2 + 3); END.") == {'x': -5.0}

    def test_assignment(self, interpreter):
      result = interpreter.eval("BEGIN x := 5; y := x + 2; END.")
      assert result == {'x': 5.0, 'y': 7.0}

    def test_empty(self, interpreter):
        assert interpreter.eval("BEGIN ; END.") == {}

    def test_multiple_statements(self, interpreter):
         result = interpreter.eval("BEGIN x := 10; y := 20; z := x + y; END.")
         assert result == {'x': 10.0, 'y': 20.0, 'z': 30.0}

    def test_uninitialized_variable(self, interpreter):
        with pytest.raises(ValueError, match="Uninitialized variable"):
            interpreter.eval("BEGIN x := y; END.")

    def test_invalid_syntax(self, interpreter):
      with pytest.raises(SyntaxError, match="Invalid token order"):
            interpreter.eval("BEGIN x 2; END.")