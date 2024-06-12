# Archivo: Metodos/Modelo/InterfazCeros.py

import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definiciones de funciones para encontrar ceros utilizando los métodos numéricos
x = sp.symbols("x")

def bisection(f, a, b, tol=1e-5):
    if f(a) * f(b) > 0:
        return None, "La función no cambia de signo en el intervalo dado"
    else:
        while abs(b - a) > tol:
            c = (a + b) / 2
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return c, None

def false_position(f, a, b, tol=1e-5):
    if f(a) * f(b) > 0:
        return None, "La función no cambia de signo en el intervalo dado"
    else:
        while True:
            c = a - (f(a) * (a - b)) / (f(a) - f(b))
            if abs(f(c)) <= tol:
                return c, None
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c

def newton(f_expr, xo, tol):
    df = sp.diff(f_expr, x)
    newton_method = x - f_expr / df
    newton_method = sp.lambdify(x, newton_method, "numpy")
    while True:
        x1 = newton_method(xo)
        if abs(x1 - xo) <= tol:
            return x1, None
        xo = x1

def secante(f, x0, x1, tol):
    try:
        while abs(x1 - x0) > tol:
            f_x0 = f(x0)
            f_x1 = f(x1)

            if f_x1 == f_x0:
                return None, "Error: División por cero en la función secante."

            x0, x1 = x1, x1 - f_x1 * ((x1 - x0) / (f_x1 - f_x0))

        return x1, None
    except ZeroDivisionError:
        return None, "Error: División por cero."
    except TypeError as e:
        return None, f"Error de tipo: {e}"

# Interfaz gráfica
class InterfazCeros:
    def __init__(self, root):
        self.root = root
        self.root.title("Ceros de Funciones")

        tk.Button(root, text="Bisección", command=self.abrir_biseccion).pack()
        tk.Button(root, text="Falsa Posición", command=self.abrir_falsa_posicion).pack()
        tk.Button(root, text="Newton", command=self.abrir_newton).pack()
        tk.Button(root, text="Secante", command=self.abrir_secante).pack()

    def abrir_biseccion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Bisección")

        tk.Label(ventana, text="Función:").grid(row=0, column=0)
        entrada_funcion = tk.Entry(ventana)
        entrada_funcion.grid(row=0, column=1)

        tk.Label(ventana, text="a:").grid(row=1, column=0)
        entrada_a = tk.Entry(ventana)
        entrada_a.grid(row=1, column=1)

        tk.Label(ventana, text="b:").grid(row=2, column=0)
        entrada_b = tk.Entry(ventana)
        entrada_b.grid(row=2, column=1)

        tk.Label(ventana, text="Tolerancia:").grid(row=3, column=0)
        entrada_tolerancia = tk.Entry(ventana)
        entrada_tolerancia.grid(row=3, column=1)

        def calcular_biseccion():
            funcion = entrada_funcion.get()
            a = float(entrada_a.get())
            b = float(entrada_b.get())
            tol = float(entrada_tolerancia.get())

            try:
                f_expr = sp.sympify(funcion)
                f = sp.lambdify(x, f_expr, "numpy")
                raiz, error = bisection(f, a, b, tol)
                if error:
                    messagebox.showerror("Error", error)
                else:
                    messagebox.showinfo("Resultado", f"Raíz: {raiz}")
                    self.graficar_funcion(f_expr, a, b, raiz, "Bisección")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_biseccion).grid(row=4, columnspan=2)

    def abrir_falsa_posicion(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Falsa Posición")

        tk.Label(ventana, text="Función:").grid(row=0, column=0)
        entrada_funcion = tk.Entry(ventana)
        entrada_funcion.grid(row=0, column=1)

        tk.Label(ventana, text="a:").grid(row=1, column=0)
        entrada_a = tk.Entry(ventana)
        entrada_a.grid(row=1, column=1)

        tk.Label(ventana, text="b:").grid(row=2, column=0)
        entrada_b = tk.Entry(ventana)
        entrada_b.grid(row=2, column=1)

        tk.Label(ventana, text="Tolerancia:").grid(row=3, column=0)
        entrada_tolerancia = tk.Entry(ventana)
        entrada_tolerancia.grid(row=3, column=1)

        def calcular_falsa_posicion():
            funcion = entrada_funcion.get()
            a = float(entrada_a.get())
            b = float(entrada_b.get())
            tol = float(entrada_tolerancia.get())

            try:
                f_expr = sp.sympify(funcion)
                f = sp.lambdify(x, f_expr, "numpy")
                raiz, error = false_position(f, a, b, tol)
                if error:
                    messagebox.showerror("Error", error)
                else:
                    messagebox.showinfo("Resultado", f"Raíz: {raiz}")
                    self.graficar_funcion(f_expr, a, b, raiz, "Falsa Posición")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_falsa_posicion).grid(row=4, columnspan=2)

    def abrir_newton(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Newton")

        tk.Label(ventana, text="Función:").grid(row=0, column=0)
        entrada_funcion = tk.Entry(ventana)
        entrada_funcion.grid(row=0, column=1)

        tk.Label(ventana, text="x₀:").grid(row=1, column=0)
        entrada_x0 = tk.Entry(ventana)
        entrada_x0.grid(row=1, column=1)

        tk.Label(ventana, text="Tolerancia:").grid(row=2, column=0)
        entrada_tolerancia = tk.Entry(ventana)
        entrada_tolerancia.grid(row=2, column=1)

        def calcular_newton():
            funcion = entrada_funcion.get()
            x0 = float(entrada_x0.get())
            tol = float(entrada_tolerancia.get())

            try:
                f_expr = sp.sympify(funcion)
                f = sp.lambdify(x, f_expr, "numpy")
                raiz, error = newton(f_expr, x0, tol)
                if error:
                    messagebox.showerror("Error", error)
                else:
                    messagebox.showinfo("Resultado", f"Raíz: {raiz}")
                    self.graficar_funcion(f_expr, x0 - 2, x0 + 2, raiz, "Newton")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_newton).grid(row=3, columnspan=2)

    def abrir_secante(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Secante")

        tk.Label(ventana, text="Función:").grid(row=0, column=0)
        entrada_funcion = tk.Entry(ventana)
        entrada_funcion.grid(row=0, column=1)

        tk.Label(ventana, text="x₀:").grid(row=1, column=0)
        entrada_x0 = tk.Entry(ventana)
        entrada_x0.grid(row=1, column=1)

        tk.Label(ventana, text="x₁:").grid(row=2, column=0)
        entrada_x1 = tk.Entry(ventana)
        entrada_x1.grid(row=2, column=1)

        tk.Label(ventana, text="Tolerancia:").grid(row=3, column=0)
        entrada_tolerancia = tk.Entry(ventana)
        entrada_tolerancia.grid(row=3, column=1)

        def calcular_secante():
            funcion = entrada_funcion.get()
            x0 = float(entrada_x0.get())
            x1 = float(entrada_x1.get())
            tol = float(entrada_tolerancia.get())

            try:
                f_expr = sp.sympify(funcion)
                f = sp.lambdify(x, f_expr, "numpy")
                raiz, error = secante(f, x0, x1, tol)
                if error:
                    messagebox.showerror("Error", error)
                else:
                    messagebox.showinfo("Resultado", f"Raíz: {raiz}")
                    self.graficar_funcion(f_expr, x0 - 2, x1 + 2, raiz, "Secante")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_secante).grid(row=4, columnspan=2)

    def graficar_funcion(self, f_expr, a, b, raiz, metodo):
        f = sp.lambdify(x, f_expr, "numpy")
        x_vals = np.linspace(a, b, 400)
        f_vals = f(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, f_vals, label="Función")
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(raiz, color='r', linestyle='--', label=f"Raíz ({metodo})")
        ax.legend()
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(f"Función y Raíz: {metodo}")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCeros(root)
    root.mainloop()
