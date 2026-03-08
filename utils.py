def power(x, n):
    if n == 0:
        return 1
    elif n > 0:
        return x * power(x, n - 1)

    if x<0:
        raise(ZeroDivisionError)

    return power(x, n + 1) / x