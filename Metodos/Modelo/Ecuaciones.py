import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

# Método de Euler
def metodo_euler(f, a, b, h, condicion_inicial):
    n = int((b - a) / h)
    t = np.linspace(a, b, n + 1)
    y = [condicion_inicial]
    for i in range(n):
        y.append(y[-1] + h * f(t[i], y[-1]))
    return t, y

# Método de Runge-Kutta de orden 4
def metodo_runge_kutta(f, a, b, h, condicion_inicial):
    n = int((b - a) / h)
    t = np.linspace(a, b, n + 1)
    y = [condicion_inicial]
    for i in range(n):
        k1 = h * f(t[i], y[-1])
        k2 = h * f(t[i] + h / 2, y[-1] + k1 / 2)
        k3 = h * f(t[i] + h / 2, y[-1] + k2 / 2)
        k4 = h * f(t[i] + h, y[-1] + k3)
        y.append(y[-1] + (k1 + 2 * k2 + 2 * k3 + k4) / 6)
    return t, y

# Interfaz gráfica
class InterfazEcuaciones:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos para EDOs")

        tk.Label(root, text="Ecuación diferencial:").grid(row=0, column=0)
        self.entrada_funcion = tk.Entry(root)
        self.entrada_funcion.grid(row=0, column=1)

        tk.Label(root, text="a:").grid(row=1, column=0)
        self.entrada_a = tk.Entry(root)
        self.entrada_a.grid(row=1, column=1)

        tk.Label(root, text="b:").grid(row=2, column=0)
        self.entrada_b = tk.Entry(root)
        self.entrada_b.grid(row=2, column=1)

        tk.Label(root, text="h:").grid(row=3, column=0)
        self.entrada_h = tk.Entry(root)
        self.entrada_h.grid(row=3, column=1)

        tk.Label(root, text="Condición inicial:").grid(row=4, column=0)
        self.entrada_ci = tk.Entry(root)
        self.entrada_ci.grid(row=4, column=1)

        tk.Button(root, text="Método de Euler", command=self.calcular_euler).grid(row=5, column=0, pady=10)
        tk.Button(root, text="Runge-Kutta de Orden 4", command=self.calcular_runge_kutta).grid(row=5, column=1, pady=10)

    def obtener_entradas(self):
        try:
            funcion = self.entrada_funcion.get()
            a = float(self.entrada_a.get())
            b = float(self.entrada_b.get())
            h = float(self.entrada_h.get())
            ci = float(self.entrada_ci.get())
            f = eval(f"lambda t, y: {funcion}")
            return f, a, b, h, ci
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return None, None, None, None, None

    def calcular_euler(self):
        f, a, b, h, ci = self.obtener_entradas()
        if f is not None:
            t, y = metodo_euler(f, a, b, h, ci)
            self.mostrar_grafica(t, y, "Método de Euler")

    def calcular_runge_kutta(self):
        f, a, b, h, ci = self.obtener_entradas()
        if f is not None:
            t, y = metodo_runge_kutta(f, a, b, h, ci)
            self.mostrar_grafica(t, y, "Runge-Kutta de Orden 4")

    def mostrar_grafica(self, t, y, metodo):
        plt.figure()
        plt.plot(t, y, label=metodo)
        plt.xlabel('t')
        plt.ylabel('y')
        plt.title(f'Solución usando {metodo}')
        plt.legend()
        plt.grid(True)
        plt.show()

# Crear ventana principal
root = tk.Tk()
app = InterfazEcuaciones(root)
root.mainloop()
