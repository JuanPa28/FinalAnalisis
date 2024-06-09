import tkinter as tk
from tkinter import messagebox
import sympy as sp
import numpy as np

# Importar los métodos de los otros módulos
from Metodos.Modelo.Ceros import *
from Metodos.Modelo.Ecuaciones import *
from Metodos.Modelo.Interpolacion import *
from Metodos.Modelo.Sistemas_ecuaciones_lineales import *
from Metodos.Modelo.Serie_teylor import *


class InterfazMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Menú Principal")

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.metodos_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Métodos", menu=self.metodos_menu)

        # Añadir los submenús y comandos correspondientes
        self.crear_submenu("Serie de Taylor", self.abrir_serie_taylor)
        self.crear_submenu("Ceros de Funciones", self.abrir_ceros_funciones)
        self.crear_submenu("Interpolación y Ajuste", self.abrir_interpolacion_ajuste)
        self.crear_submenu("Ecuaciones Diferenciales", self.abrir_ecuaciones_diferenciales)
        self.crear_submenu("Sistemas de Ecuaciones Lineales", self.abrir_sistemas_ecuaciones_lineales)

        # Inicializar frames para cada opción de la interfaz
        self.frames = {}
        self.crear_interfaz_serie_taylor()
        self.crear_interfaz_ceros_funciones()
        self.crear_interfaz_interpolacion_ajuste()
        self.crear_interfaz_ecuaciones_diferenciales()
        self.crear_interfaz_sistemas_ecuaciones_lineales()

    def crear_submenu(self, label, command):
        self.metodos_menu.add_command(label=label, command=command)

    def limpiar_area_trabajo(self):
        for frame in self.frames.values():
            frame.pack_forget()

    def crear_frame(self, name):
        self.frames[name] = tk.Frame(self.root)

    def abrir_serie_taylor(self):
        self.limpiar_area_trabajo()
        self.frames["SerieTaylor"].pack()

    def abrir_ceros_funciones(self):
        self.limpiar_area_trabajo()
        self.frames["CerosFunciones"].pack()

    def abrir_interpolacion_ajuste(self):
        self.limpiar_area_trabajo()
        self.frames["InterpolacionAjuste"].pack()

    def abrir_ecuaciones_diferenciales(self):
        self.limpiar_area_trabajo()
        self.frames["EcuacionesDiferenciales"].pack()

    def abrir_sistemas_ecuaciones_lineales(self):
        self.limpiar_area_trabajo()
        self.frames["SistemasEcuacionesLineales"].pack()

    def crear_interfaz_serie_taylor(self):
        self.crear_frame("SerieTaylor")
        frame = self.frames["SerieTaylor"]
        tk.Label(frame, text="Función:").grid(row=0, column=0)
        self.entry_funcion = tk.Entry(frame)
        self.entry_funcion.grid(row=0, column=1)

        tk.Label(frame, text="Grado:").grid(row=1, column=0)
        self.entry_grado = tk.Entry(frame)
        self.entry_grado.grid(row=1, column=1)

        tk.Button(frame, text="Calcular Polinomio de Taylor", command=self.calcular_polinomio_taylor).grid(row=2, columnspan=2)

    def calcular_polinomio_taylor(self):
        funcion = self.entry_funcion.get()
        grado = int(self.entry_grado.get())

        try:
            x = sp.symbols('x')
            f = eval(funcion)
            polinomio = taylor(f, 0, grado)

            messagebox.showinfo("Polinomio de Taylor", f"El polinomio de Taylor es: {polinomio}")

            # Mostrar gráfica de la función y el polinomio de Taylor
            graficar_serie_taylor(f, 0, grado)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def crear_interfaz_ceros_funciones(self):
        self.crear_frame("CerosFunciones")
        frame = self.frames["CerosFunciones"]
        tk.Label(frame, text="Función:").grid(row=0, column=0)
        self.entry_funcion_ceros = tk.Entry(frame)
        self.entry_funcion_ceros.grid(row=0, column=1)

        tk.Label(frame, text="Intervalo (a, b):").grid(row=1, column=0)
        self.entry_intervalo_a = tk.Entry(frame, width=5)
        self.entry_intervalo_a.grid(row=1, column=1)
        tk.Label(frame, text=",").grid(row=1, column=2)
        self.entry_intervalo_b = tk.Entry(frame, width=5)
        self.entry_intervalo_b.grid(row=1, column=3)

        tk.Label(frame, text="Exactitud:").grid(row=2, column=0)
        self.entry_exactitud = tk.Entry(frame)
        self.entry_exactitud.grid(row=2, column=1)

        tk.Label(frame, text="Método:").grid(row=3, column=0)
        self.metodo_ceros = tk.StringVar(frame)
        self.metodo_ceros.set("Bisección")
        metodo_menu = tk.OptionMenu(frame, self.metodo_ceros,
                                    ("Bisección", lambda: self.calcular_ceros_biseccion()),
                                    ("Newton", lambda: self.calcular_ceros_newton()),
                                    ("Falsa Posición", lambda: self.calcular_ceros_falsa_posicion()),
                                    ("Secante", lambda: self.calcular_ceros_secante()))
        metodo_menu.grid(row=3, column=1)

        tk.Button(frame, text="Calcular Ceros", command=self.calcular_ceros).grid(row=4, columnspan=4)

    def calcular_ceros(self):
        funcion = self.entry_funcion_ceros.get()
        a = float(self.entry_intervalo_a.get())
        b = float(self.entry_intervalo_b.get())
        exactitud = float(self.entry_exactitud.get())
        metodo = self.metodo_ceros.get()

        try:
            x = sp.symbols('x')
            f_sympy = eval(funcion)
            f = sp.lambdify(x, f_sympy, 'numpy')

            if metodo == "Bisección":
                ceros, iteraciones = bisection(f, a, b, exactitud)
            elif metodo == "Newton":
                ceros, iteraciones = newton(f_sympy, a, exactitud)
            elif metodo == "Falsa Posición":
                ceros, iteraciones = false_position(f, a, b, exactitud)
            elif metodo == "Secante":
                ceros, iteraciones = secante(f, a, b, exactitud)

            messagebox.showinfo("Ceros de Funciones",
                                f"Método: {metodo}\n"
                                f"Cero: {ceros} (Iteraciones: {iteraciones})")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def crear_interfaz_interpolacion_ajuste(self):
        self.crear_frame("InterpolacionAjuste")
        frame = self.frames["InterpolacionAjuste"]
        tk.Label(frame, text="Datos de x:").grid(row=0, column=0)
        self.entry_datos_x = tk.Entry(frame)
        self.entry_datos_x.grid(row=0, column=1)

        tk.Label(frame, text="Datos de y:").grid(row=1, column=0)
        self.entry_datos_y = tk.Entry(frame)
        self.entry_datos_y.grid(row=1, column=1)

        tk.Label(frame, text="Valor de x para aproximar:").grid(row=2, column=0)
        self.entry_x_aprox = tk.Entry(frame)
        self.entry_x_aprox.grid(row=2, column=1)

        tk.Label(frame, text="Método:").grid(row=3, column=0)
        self.metodo_interpolacion = tk.StringVar(frame)
        self.metodo_interpolacion.set("Polinomio Simple")
        metodo_menu = tk.OptionMenu(frame, self.metodo_interpolacion, "Polinomio Simple", "Lagrange")
        metodo_menu.grid(row=3, column=1)

        tk.Button(frame, text="Calcular Interpolación", command=self.mostrar_campos_interpolacion).grid(row=4, columnspan=2)

    def mostrar_campos_interpolacion(self):
        metodo = self.metodo_interpolacion.get()
        if metodo == "Polinomio Simple":
            self.calcular_interpolacion()
        elif metodo == "Lagrange":
            self.calcular_interpolacion()

    def calcular_interpolacion(self):
        datos_x = list(map(float, self.entry_datos_x.get().split(',')))
        datos_y = list(map(float, self.entry_datos_y.get().split(',')))
        x_aprox = float(self.entry_x_aprox.get())
        metodo = self.metodo_interpolacion.get()

        try:
            if metodo == "Polinomio Simple":
                interpolacion = polinomio_simple(datos_x, datos_y)
            elif metodo == "Lagrange":
                interpolacion = interp_lagrange(datos_x, datos_y)

            y_aprox = interpolacion(x_aprox)

            messagebox.showinfo("Interpolación y Ajuste",
                                f"Método: {metodo}\n"
                                f"Aproximación en x={x_aprox}: {y_aprox}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def crear_interfaz_ecuaciones_diferenciales(self):
        self.crear_frame("EcuacionesDiferenciales")
        frame = self.frames["EcuacionesDiferenciales"]
        tk.Label(frame, text="Función f(x,y):").grid(row=0, column=0)
        self.entry_funcion_ecuaciones_diferenciales = tk.Entry(frame)
        self.entry_funcion_ecuaciones_diferenciales.grid(row=0, column=1)

        tk.Label(frame, text="Valor inicial x0:").grid(row=1, column=0)
        self.entry_x0_ecuaciones_diferenciales = tk.Entry(frame)
        self.entry_x0_ecuaciones_diferenciales.grid(row=1, column=1)

        tk.Label(frame, text="Valor inicial y0:").grid(row=2, column=0)
        self.entry_y0_ecuaciones_diferenciales = tk.Entry(frame)
        self.entry_y0_ecuaciones_diferenciales.grid(row=2, column=1)

        tk.Label(frame, text="Valor de x para aproximar:").grid(row=3, column=0)
        self.entry_x_aprox_ecuaciones_diferenciales = tk.Entry(frame)
        self.entry_x_aprox_ecuaciones_diferenciales.grid(row=3, column=1)

        tk.Label(frame, text="Método:").grid(row=4, column=0)
        self.metodo_ecuaciones_diferenciales = tk.StringVar(frame)
        self.metodo_ecuaciones_diferenciales.set("Euler")
        metodo_menu = tk.OptionMenu(frame, self.metodo_ecuaciones_diferenciales, "Euler", "Runge-Kutta")
        metodo_menu.grid(row=4, column=1)

        tk.Button(frame, text="Calcular Ecuación Diferencial", command=self.calcular_ecuaciones_diferenciales).grid(
            row=5, columnspan=2)

    def calcular_ecuaciones_diferenciales(self):
        funcion = self.entry_funcion_ecuaciones_diferenciales.get()
        x0 = float(self.entry_x0_ecuaciones_diferenciales.get())
        y0 = float(self.entry_y0_ecuaciones_diferenciales.get())
        x_aprox = float(self.entry_x_aprox_ecuaciones_diferenciales.get())
        metodo = self.metodo_ecuaciones_diferenciales.get()

        try:
            f = eval(funcion)

            if metodo == "Euler":
                resultado = metodo_euler(f, x0, y0, x_aprox)
            elif metodo == "Runge-Kutta":
                resultado = metodo_runge_kutta(f, x0, y0, x_aprox)

            messagebox.showinfo("Ecuación Diferencial",
                                f"Método: {metodo}\n"
                                f"El resultado en x={x_aprox} es y={resultado[-1]}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def crear_interfaz_sistemas_ecuaciones_lineales(self):
        self.crear_frame("SistemasEcuacionesLineales")
        frame = self.frames["SistemasEcuacionesLineales"]
        tk.Label(frame, text="Matriz de coeficientes (A):").grid(row=0, column=0)
        self.entry_matriz_sistemas = tk.Text(frame, width=20, height=5)
        self.entry_matriz_sistemas.grid(row=0, column=1)

        tk.Label(frame, text="Vector de términos independientes (B):").grid(row=1, column=0)
        self.entry_vector_sistemas = tk.Text(frame, width=20, height=5)
        self.entry_vector_sistemas.grid(row=1, column=1)

        tk.Label(frame, text="Tolerancia:").grid(row=2, column=0)
        self.entry_tol_sistemas = tk.Entry(frame)
        self.entry_tol_sistemas.grid(row=2, column=1)

        tk.Label(frame, text="Método:").grid(row=3, column=0)
        self.metodo_sistemas_ecuaciones = tk.StringVar(frame)
        self.metodo_sistemas_ecuaciones.set("Gauss-Seidel")
        metodo_menu = tk.OptionMenu(frame, self.metodo_sistemas_ecuaciones, "Gauss-Seidel", "Jacobi")
        metodo_menu.grid(row=3, column=1)

        tk.Button(frame, text="Calcular Solución", command=self.calcular_sistemas_ecuaciones).grid(row=4, columnspan=2)

    def calcular_sistemas_ecuaciones(self):
        matriz_str = self.entry_matriz_sistemas.get("1.0", tk.END)
        vector_str = self.entry_vector_sistemas.get("1.0", tk.END)
        tolerancia = float(self.entry_tol_sistemas.get())
        metodo = self.metodo_sistemas_ecuaciones.get()

        try:
            matriz = np.array([[float(num) for num in fila.split()] for fila in matriz_str.splitlines()])
            vector = np.array([float(num) for num in vector_str.split()])

            if metodo == "Gauss-Seidel":
                solucion = G_seidel(matriz, vector, np.zeros(len(vector)), tolerancia)[0]


            messagebox.showinfo("Sistemas de Ecuaciones Lineales",
                                f"Método: {metodo}\n"
                                f"La solución es: {', '.join(str(num) for num in solucion)}")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


root = tk.Tk()
app = InterfazMenu(root)
root.mainloop()