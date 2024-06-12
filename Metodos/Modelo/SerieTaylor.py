import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import factorial

# Definiciones de funciones para la Serie de Taylor
x = sp.symbols('x')

def taylor(f, x0, n):
    p = 0
    for k in range(0, n + 1):
        df = sp.diff(f, x, k)
        df_x0 = df.evalf(subs={x: x0})
        T = (df_x0 * (x - x0) ** k) / factorial(k)
        p = p + T
    return p
def graficar_serie_taylor(f, x0, n):
    P = taylor(f, x0, n)
    P_func = sp.lambdify(x, P)
    x_vals = np.linspace(x0 - 2, x0 + 2, 400)
    f_vals = sp.lambdify(x, f)(x_vals)
    P_vals = P_func(x_vals)

    plt.figure()
    plt.plot(x_vals, f_vals, label='Función Original')
    plt.plot(x_vals, P_vals, label=f'Polinomio de Taylor (grado {n})', linestyle='--')
    plt.title('Serie de Taylor')
    plt.legend()
    plt.show()

# Interfaz gráfica
class InterfazTaylor:
    def __init__(self, root):
        self.root = root
        self.root.title("Serie de Taylor")

        tk.Label(root, text="Función:").grid(row=0, column=0)
        self.entry_funcion = tk.Entry(root)
        self.entry_funcion.grid(row=0, column=1)

        tk.Label(root, text="Punto x₀:").grid(row=1, column=0)
        self.entry_x0 = tk.Entry(root)
        self.entry_x0.grid(row=1, column=1)

        tk.Label(root, text="Grado:").grid(row=2, column=0)
        self.entry_grado = tk.Entry(root)
        self.entry_grado.grid(row=2, column=1)

        tk.Button(root, text="Calcular Polinomio de Taylor", command=self.calcular_polinomio_taylor).grid(row=3, columnspan=2)

    def calcular_polinomio_taylor(self):
        funcion = self.entry_funcion.get()
        x0 = float(self.entry_x0.get())
        grado = int(self.entry_grado.get())

        try:
            f = eval(funcion)
            polinomio = taylor(f, x0, grado)

            messagebox.showinfo("Polinomio de Taylor", f"El polinomio de Taylor es: {polinomio}")

            self.graficar_serie_taylor(f, polinomio, x0, grado)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def graficar_serie_taylor(self, funcion, polinomio, x0, grado):
        x_vals = np.linspace(x0 - 2, x0 + 2, 400)
        f_vals = sp.lambdify(x, funcion, 'numpy')(x_vals)
        P_vals = sp.lambdify(x, polinomio, 'numpy')(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, f_vals, label='Función Original')
        ax.plot(x_vals, P_vals, label=f'Polinomio de Taylor (grado {grado})', linestyle='--')
        ax.legend()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Serie de Taylor')

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazTaylor(root)
    root.mainloop()
