import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def metodo_euler(f, a, b, h, condicion_inicial):
    # Método de Euler
    n = int((b - a) / h)
    t = np.linspace(a, b, n + 1)
    y_euler = [condicion_inicial]
    for i in range(n):
        y_euler.append(y_euler[i] + h * f(t[i], y_euler[i]))
    return t, y_euler

def metodo_runge_kutta(f, a, b, h, condicion_inicial):
    # Método de Runge-Kutta de cuarto orden
    n = int((b - a) / h)
    t = np.linspace(a, b, n + 1)
    y_rk = [condicion_inicial]
    for i in range(n):
        k1 = h * f(t[i], y_rk[i])
        k2 = h * f(t[i] + 0.5 * h, y_rk[i] + 0.5 * k1)
        k3 = h * f(t[i] + 0.5 * h, y_rk[i] + 0.5 * k2)
        k4 = h * f(t[i] + h, y_rk[i] + k3)
        y_rk.append(y_rk[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    return t, y_rk

def runge_kutta_4(f, a, b, h, valores_iniciales, params):
    # Método de Runge-Kutta de cuarto orden modificado
    n = int((b - a) / h)
    t = np.linspace(a, b, n + 1)
    uv = np.array([valores_iniciales])

    for i in range(n):
        k1 = h * f(t[i], uv[i], *params)
        k2 = h * f(t[i] + h / 2, uv[i] + 1 / 2 * k1, *params)
        k3 = h * f(t[i] + h / 2, uv[i] + 1 / 2 * k2, *params)
        k4 = h * f(t[i + 1], uv[i] + k3, *params)
        uv_nuevo = uv[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        uv = np.vstack([uv, uv_nuevo])

    return t, uv
