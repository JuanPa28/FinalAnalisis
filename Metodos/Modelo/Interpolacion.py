import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy as sp

X = sp.symbols('x')

def polinomio_simple(x_dato, y_dato):
    N = len(x_dato)
    M = np.zeros([N, N])
    P = 0

    for i in range(N):
        M[i, 0] = 1
        for j in range(1, N):
            M[i, j] = M[i, j - 1] * x_dato[i]

    ai = np.linalg.solve(M, y_dato)

    for i in range(N):
        P += ai[i] * X ** i

    resultado = f"El polinomio interpolante es: P(X) = {P}"
    return sp.lambdify(X, P), resultado

def interp_lagrange(x_dato, y_dato):
    N = len(x_dato)
    P = 0

    for i in range(N):
        T = 1
        for j in range(N):
            if j != i:
                T *= (X - x_dato[j]) / (x_dato[i] - x_dato[j])
        P += T * y_dato[i]

    resultado = f"El polinomio es P(X) = {sp.expand(P)}"
    return sp.lambdify(X, P), resultado

def ajuste_minimos_cuadrados(x_dato, y_dato, grado):
    A = np.vander(x_dato, grado + 1)
    coeficientes = np.linalg.lstsq(A, y_dato, rcond=None)[0]
    p = np.poly1d(coeficientes[::-1])
    resultado = f"El polinomio de ajuste es: {p}"
    return p, resultado

def modelo_potencias(x, a, b):
    return a * x ** b

class InterfazInterpolacionAjuste:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolación y Ajuste de Curva")

        tk.Button(root, text="Interpolación Polinómica Simple", command=self.abrir_polinomio_simple).pack()
        tk.Button(root, text="Interpolación de Lagrange", command=self.abrir_interp_lagrange).pack()
        tk.Button(root, text="Ajuste de Mínimos Cuadrados", command=self.abrir_ajuste_minimos_cuadrados).pack()

    def abrir_polinomio_simple(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Interpolación Polinómica Simple")

        tk.Label(ventana, text="Datos X (separados por comas):").grid(row=0, column=0)
        entrada_x = tk.Entry(ventana)
        entrada_x.grid(row=0, column=1)

        tk.Label(ventana, text="Datos Y (separados por comas):").grid(row=1, column=0)
        entrada_y = tk.Entry(ventana)
        entrada_y.grid(row=1, column=1)

        def calcular_polinomio_simple():
            x_dato = np.fromstring(entrada_x.get(), sep=',')
            y_dato = np.fromstring(entrada_y.get(), sep=',')
            try:
                f, resultado = polinomio_simple(x_dato, y_dato)
                messagebox.showinfo("Resultado", resultado)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_polinomio_simple).grid(row=2, columnspan=2)

    def abrir_interp_lagrange(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Interpolación de Lagrange")

        tk.Label(ventana, text="Datos X (separados por comas):").grid(row=0, column=0)
        entrada_x = tk.Entry(ventana)
        entrada_x.grid(row=0, column=1)

        tk.Label(ventana, text="Datos Y (separados por comas):").grid(row=1, column=0)
        entrada_y = tk.Entry(ventana)
        entrada_y.grid(row=1, column=1)

        def calcular_interp_lagrange():
            x_dato = np.fromstring(entrada_x.get(), sep=',')
            y_dato = np.fromstring(entrada_y.get(), sep=',')
            try:
                f, resultado = interp_lagrange(x_dato, y_dato)
                messagebox.showinfo("Resultado", resultado)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_interp_lagrange).grid(row=2, columnspan=2)

    def abrir_ajuste_minimos_cuadrados(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Ajuste de Mínimos Cuadrados")

        tk.Label(ventana, text="Datos X (separados por comas):").grid(row=0, column=0)
        entrada_x = tk.Entry(ventana)
        entrada_x.grid(row=0, column=1)

        tk.Label(ventana, text="Datos Y (separados por comas):").grid(row=1, column=0)
        entrada_y = tk.Entry(ventana)
        entrada_y.grid(row=1, column=1)

        tk.Label(ventana, text="Grado del polinomio:").grid(row=2, column=0)
        entrada_grado = tk.Entry(ventana)
        entrada_grado.grid(row=2, column=1)

        def calcular_ajuste_minimos_cuadrados():
            x_dato = np.fromstring(entrada_x.get(), sep=',')
            y_dato = np.fromstring(entrada_y.get(), sep=',')
            grado = int(entrada_grado.get())
            try:
                p, resultado = ajuste_minimos_cuadrados(x_dato, y_dato, grado)
                messagebox.showinfo("Resultado", resultado)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_ajuste_minimos_cuadrados).grid(row=3, columnspan=2)

# Crear ventana principal
root = tk.Tk()
app = InterfazInterpolacionAjuste(root)
root.mainloop()
