import numpy as np
import sympy as sp

def false_position(f, a, b, tol=1e-5):
    if (f(a) * f(b) > 0):
        print(f"La función no cumple el teorema en el intervalo {[a, b]}.")
        return False, False
    else:
        c = a - ((f(a) * (a - b)) / (f(a) - f(b)))
        count = 0
        while (np.abs(f(c)) > tol):
            c = a - ((f(a) * (a - b)) / (f(a) - f(b)))
            if (f(a) * f(c) < 0):
                b = c
            else:
                a = c
            count += 1
    return c, count

def bisection(f, a, b, tol=1e-5):
    if (f(a) * f(b) > 0):
        return '', 'La función no cumple el teorema en el intervalo'
    else:
        i = 0
        while (np.abs(b - a > tol)):
            c = (a + b) / 2
            if (f(a) * f(c) < 0):
                b = c
                i += 1
            else:
                a = c
                i += 1

    return c, i

def newton(f, xo, tol):
    x = sp.symbols('x')
    df = sp.diff(f, x)
    N = x - f / df
    N = sp.lambdify(x, N)
    x1 = N(xo)
    count = 0
    while (np.abs(x1 - xo) > tol):
        count += 1
        xo = x1
        x1 = N(xo)
    return x1, count

def secante(f, xo, x1, tol):
    x2 = x1 - f(x1) * (xo - x1) / (f(xo) - f(x1))
    count = 0
    while (np.abs(x2 - x1) > tol):
        count += 1
        xo = x1
        x1 = x2
        x2 = x1 - f(x1) * (xo - x1) / (f(xo) - f(x1))
    return x2, count
