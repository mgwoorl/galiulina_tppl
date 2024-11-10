import pytest
from notation.notation import notation

class TestNotation:
    @pytest.mark.parametrize(
        "expr, notation_res",
        [
            ("+ - 13 4 55", "((13 - 4) + 55)"),
            ("+ 9 * 2 3", "(9 + (2 * 3))"),
            ("/ + 1 2 3", "((1 + 2) / 3)")
        ]
    )

    def test_with_diff_operators(self, expr, notation_res):
        assert notation(expr) == notation_res

    def test_expr_len_err(self):
        with pytest.raises(SyntaxError):
            notation("1 2")

    def test_unknown_symbol(self):
        with pytest.raises(SyntaxError):
            notation("% 1 2")

    def test_incorrect_number_of_nums(self):
        with pytest.raises(ValueError):
            notation("+ + 3")
