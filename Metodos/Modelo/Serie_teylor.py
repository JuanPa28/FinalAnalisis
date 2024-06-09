import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from math import factorial

x = sp.symbols('x')

def taylor(f, x0, n):
    p = 0
    for k in range(0, n + 1):
        df = sp.diff(f, x, k)
        df_x0 = df.evalf(subs={x: x0})
        T = (df_x0 * (x - x0) ** k) / factorial(k)
        p = p + T
    return p

def cota_error(f, px, x0, n):
    M = max(x0, px)
    m = min(x0, px)
    w = np.linspace(m, M, 1000)
    dfn = sp.lambdify(x, sp.diff(f, x, n + 1))
    ma = np.max(np.abs(dfn(w)))
    c = ma * (px - x0) ** (n + 1) / factorial(n + 1)
    return c

def graficar_serie_taylor(f, x0, n):
    # Calcula el polinomio de Taylor
    P = taylor(f, x0, n)

    # Crea una función lambda a partir del polinomio de Taylor
    P_func = sp.lambdify(x, P)

    # Crea un rango de valores para x
    x_vals = np.linspace(x0 - 2, x0 + 2, 400)

    # Evalúa la función original y el polinomio de Taylor en los valores de x
    f_vals = sp.lambdify(x, f)(x_vals)
    P_vals = P_func(x_vals)

    # Grafica la función original y el polinomio de Taylor
    plt.plot(x_vals, f_vals, label='Función Original')
    plt.plot(x_vals, P_vals, label=f'Polinomio de Taylor (grado {n})')

    # Añade título y leyenda al gráfico
    plt.title('Serie de Taylor')
    plt.legend()

    # Muestra la gráfica
    plt.show()
