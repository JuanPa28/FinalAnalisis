import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy as sp

# Definiciones de funciones para encontrar ceros utilizando los nuevos métodos
x = sp.symbols("x")

def bisection(f, a, b, tol=1e-5):
    if f(a) * f(b) > 0:
        return None, "La función no cumple el teorema en el intervalo"
    else:
        while np.abs(b - a) > tol:
            c = (a + b) / 2
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
    return c

def false_position(f, a, b, tol=1e-5):
    if f(a) * f(b) > 0:
        return None, "La función no cumple el teorema en el intervalo"
    else:
        while True:
            c = a - ((f(a) * (a - b)) / (f(a) - f(b)))
            if np.abs(f(c)) <= tol:
                break
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return c

def newton(f, xo, tol):
    df = sp.diff(f, x)
    newton_method = x - f / df
    newton_method = sp.lambdify(x, newton_method)
    i = 1
    while True:
        x1 = newton_method(xo)
        if np.abs(x1 - xo) <= tol:
            break
        xo = x1
        i += 1
    return x1, i

def secante(f, xo, x1, tol):
    try:
        x2 = x1 - f(x1) * (x1 - xo) / (f(xo) - f(x1))
        while np.abs(x2 - x1) > tol:
            xo = x1
            x1 = x2
            x2 = x1 - f(x1) * (xo - x1) / (f(xo) - f(x1))
        return x2
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
                f = eval("lambda x: " + funcion, {"x": x})
                raiz = bisection(f, a, b, tol)
                if raiz is None:
                    messagebox.showerror("Error", "La función no cumple el teorema en el intervalo")
                else:
                    messagebox.showinfo("Resultado", f"Raíz: {raiz}")
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
                f = eval("lambda x: " + funcion)
                raiz = false_position(f, a, b, tol)
                if raiz is None:
                    messagebox.showerror("Error", "La función no cumple el teorema en el intervalo")
                else:
                    messagebox.showinfo("Resultado", f"Raíz: {raiz}")
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
                f = eval(funcion, {"x": x})
                raiz, iteraciones = newton(f, x0, tol)
                messagebox.showinfo("Resultado", f"Raíz: {raiz}\nIteraciones: {iteraciones}")
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
                f = eval("lambda x: " + funcion)
                raiz = secante(f, x0, x1, tol)
                if raiz is None:
                    messagebox.showerror("Error", "Ocurrió un error en el cálculo")
                else:
                    messagebox.showinfo("Resultado", f"Raíz: {raiz}")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        tk.Button(ventana, text="Calcular", command=calcular_secante).grid(row=4, columnspan=2)

# Crear ventana principal
root = tk.Tk()
app = InterfazCeros(root)
root.mainloop()
