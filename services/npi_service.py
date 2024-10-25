def evaluate_rpn(expression):
    stack = []
    tokens = expression.split()

    operations = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b if b != 0 else (_ for _ in ()).throw(ValueError("Error: division by zero"))
    }

    for token in tokens:
        if token not in operations:
            stack.append(float(token))
        else:
            if len(stack) < 2:
                raise ValueError("Error: invalid RPN expression")
            b, a = stack.pop(), stack.pop()
            stack.append(operations[token](a, b))

    if len(stack) != 1:
        raise ValueError("Error: invalid RPN expression")
    return stack[0]
