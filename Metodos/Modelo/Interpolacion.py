import numpy as np
import sympy as sp
from math import factorial

X = sp.symbols('x')

def polinomio_simple(x_dato, y_dato):
    # Interpolación polinómica simple
    N = len(x_dato)
    M = np.zeros([N, N])
    P = 0

    for i in range(N):
        M[i, 0] = 1  # Inicializa la primera columna de M con 1
        for j in range(1, N):
            M[i, j] = M[i, j - 1] * x_dato[i]  # Calcula los elementos restantes de M

    ai = np.linalg.solve(M, y_dato)  # Resuelve el sistema lineal para encontrar coeficientes

    for i in range(N):
        P += ai[i] * X ** i  # Construye el polinomio interpolante

    print('El polinomio interpolante es: P(X) =', P)
    return sp.lambdify(X, P)  # Retorna una función que evalúa el polinomio


def interp_lagrange(x_dato, y_dato):
    # Interpolación de Lagrange
    N = len(x_dato)
    P = 0  # Inicializa el polinomio interpolante

    for i in range(N):
        T = 1  # Inicializa el término de Lagrange
        for j in range(N):
            if j != i:
                T *= (X - x_dato[j]) / (x_dato[i] - x_dato[j])  # Construye el término de Lagrange
        P += T * y_dato[i]  # Suma el término al polinomio

    print('El polinomio es P(X) =', sp.expand(P))
    return sp.lambdify(X, P)  # Retorna una función que evalúa el polinomio


def ajuste_minimos_cuadrados(x_dato, y_dato, grado):
    # Ajuste de mínimos cuadrados
    A = np.vander(x_dato, grado + 1)  # Crea la matriz de Vandermonde
    coeficientes = np.linalg.lstsq(A, y_dato, rcond=None)[0]  # Resuelve el sistema para encontrar los coeficientes
    p = np.poly1d(coeficientes[::-1])  # Crea un objeto polinomial con los coeficientes
    return p  # Retorna el polinomio


def ajuste_lineal_minimos_cuadrados(x, y):
    # Ajuste lineal por mínimos cuadrados
    a1, a0 = np.polyfit(x, y, 1)  # Encuentra los coeficientes del ajuste lineal
    print(f"Intercepto (a0): {a0}")
    print(f"Pendiente (a1): {a1}")
    return a0, a1  # Retorna el intercepto y la pendiente


def modelo_potencias(x, a, b):
    # Modelo de potencias
    return a * x ** b  # Retorna el valor del modelo de potencias


def cota_error(f, px, x0, n):
    M = max(x0, px)
    m = min(x0, px)
    w = np.linspace(m, M, 1000)
    df = sp.diff(f, X, n + 1)  # Definir la derivada de la función f
    dfn = sp.lambdify(X, df)
    ma = np.max(np.abs(dfn(w)))
    c = ma * (px - x0) ** (n + 1) / factorial(n + 1)
    return c
