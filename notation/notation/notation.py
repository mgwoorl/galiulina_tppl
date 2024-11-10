def notation(expr: str) -> str:
    expr = expr.split()

    if len(expr) < 3:
        raise SyntaxError("Длина выражния с оператором не может быть меньше 3")

    expr = reversed(expr)
    op = ["+", "-", "*", "/"]

    stack = []

    for i in expr:
        if i.isdigit():
            stack.append(i)

        elif i in op:
            if len(stack) < 2:
                raise ValueError(f"Недостаточно чисел, некорректно введенное выражение")

            a = stack.pop()
            b = stack.pop()

            stack.append(f"({a} {i} {b})")

        else:
            raise SyntaxError(f"Неизвестный символ")

    res_expr = stack[0]

    return res_expr
