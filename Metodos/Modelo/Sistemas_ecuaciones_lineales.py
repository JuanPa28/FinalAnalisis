import tkinter as tk
from tkinter import messagebox
import numpy as np

# Definiciones de funciones para resolver sistemas de ecuaciones lineales
def G_seidel(A, b, xo, tol):
    D = np.diag(np.diag(A))
    U = D - np.triu(A)
    L = D - np.tril(A)

    tg = np.dot(np.linalg.inv((D - L)), U)
    cg = np.dot(np.linalg.inv((D - L)), b)

    lam, _ = np.linalg.eig(tg)

    if (max(abs(lam)) < 1):
        x1 = np.dot(tg, xo) + cg
        lista = []
        while(max(abs(x1 - xo)) > tol):
            lista.append([x1, max(abs(x1 - xo))])
            xo = x1
            x1 = np.dot(tg, xo) + cg
        lista.append([x1, max(abs(x1 - xo))])
        return x1, lista
    else:
        return None, "El sistema iterativo no converge"

def Eliminacion_Gaussiana(A, b):
    n = len(b)
    x = np.zeros(n)
    for k in range(0, n - 1):
        for i in range(k + 1, n):
            lam = A[i, k] / A[k, k]
            A[i, k:n] -= lam * A[k, k:n]
            b[i] -= lam * b[k]
    for k in range(n - 1, -1, -1):
        x[k] = (b[k] - np.dot(A[k, k + 1:n], x[k + 1:n])) / A[k, k]
    return x

def Gauss_sum(A, B, X0, tol):
    n = len(B)
    norm = 2
    cont = 0
    M = 50
    X1 = np.zeros(n)
    while(norm >= tol and cont < M):
        for i in range(n):
            aux = 0
            for j in range(n):
                if (i != j):
                    aux -= A[i, j] * X0[j]
            X1[i] = (B[i] + aux) / A[i, i]
        norm = np.max(np.abs(X1 - X0))
        X0 = X1.copy()
        cont += 1
    return X1

def pivoteo(A, b):
    n = len(b)
    for i in range(n):
        max_index = abs(A[i:, i]).argmax() + i
        A[[i, max_index]] = A[[max_index, i]]
        b[[i, max_index]] = b[[max_index, i]]
    return A, b

# Interfaz gráfica
class InterfazSistemasLineales:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolución de Sistemas de Ecuaciones Lineales")

        # Lista de selección de tipo de método
        tk.Label(root, text="Selecciona el tipo de método:").pack(pady=10)
        self.metodo_tipo = tk.StringVar()
        self.metodo_tipo.set("Directo")
        self.opciones_tipo = ["Directo", "Iterativo"]
        self.menu_tipo = tk.OptionMenu(root, self.metodo_tipo, *self.opciones_tipo, command=self.actualizar_metodos)
        self.menu_tipo.pack()

        # Lista de selección de método específico
        tk.Label(root, text="Selecciona el método:").pack(pady=10)
        self.metodo = tk.StringVar()
        self.metodo.set("Eliminación Gaussiana")
        self.opciones_metodos = ["Eliminación Gaussiana", "Pivoteo"]
        self.menu_metodos = tk.OptionMenu(root, self.metodo, *self.opciones_metodos)
        self.menu_metodos.pack()

        # Entradas de matriz y vector
        tk.Label(root, text="Matriz A (fila por fila, elementos separados por comas):").pack()
        self.entrada_matriz_A = tk.Text(root, height=5, width=40)
        self.entrada_matriz_A.pack(pady=10)

        tk.Label(root, text="Vector b (elementos separados por comas):").pack()
        self.entrada_vector_b = tk.Entry(root, width=40)
        self.entrada_vector_b.pack(pady=10)

        # Campos adicionales para métodos iterativos
        self.label_xo = tk.Label(root, text="Vector inicial X0 (elementos separados por comas):")
        self.entrada_xo = tk.Entry(root, width=40)
        self.label_tol = tk.Label(root, text="Tolerancia (por ejemplo 1e-6):")
        self.entrada_tol = tk.Entry(root, width=40)

        # Botón para calcular
        tk.Button(root, text="Calcular", command=self.calcular).pack(pady=20)

    def actualizar_metodos(self, seleccion):
        if seleccion == "Directo":
            self.opciones_metodos = ["Eliminación Gaussiana", "Pivoteo"]
            self.menu_metodos['menu'].delete(0, 'end')
            for metodo in self.opciones_metodos:
                self.menu_metodos['menu'].add_command(label=metodo, command=tk._setit(self.metodo, metodo))
            self.metodo.set(self.opciones_metodos[0])
            self.label_xo.pack_forget()
            self.entrada_xo.pack_forget()
            self.label_tol.pack_forget()
            self.entrada_tol.pack_forget()
        elif seleccion == "Iterativo":
            self.opciones_metodos = ["Gauss-Seidel"]
            self.menu_metodos['menu'].delete(0, 'end')
            for metodo in self.opciones_metodos:
                self.menu_metodos['menu'].add_command(label=metodo, command=tk._setit(self.metodo, metodo))
            self.metodo.set(self.opciones_metodos[0])
            self.label_xo.pack(pady=10)
            self.entrada_xo.pack(pady=10)
            self.label_tol.pack(pady=10)
            self.entrada_tol.pack(pady=10)

    def obtener_entradas(self):
        try:
            # Obtener la matriz A
            A_texto = self.entrada_matriz_A.get("1.0", tk.END).strip()
            A_lista = [list(map(float, fila.split(','))) for fila in A_texto.split('\n') if fila.strip()]
            A = np.array(A_lista)

            # Obtener el vector b
            b_texto = self.entrada_vector_b.get().strip()
            b = np.array(list(map(float, b_texto.split(','))))

            if A.shape[0] != A.shape[1] or A.shape[0] != b.shape[0]:
                raise ValueError("Dimensiones de la matriz A y el vector b no coinciden.")

            return A, b
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return None, None

    def calcular(self):
        metodo_tipo = self.metodo_tipo.get()
        metodo = self.metodo.get()
        A, b = self.obtener_entradas()

        if A is not None and b is not None:
            try:
                if metodo_tipo == "Directo":
                    if metodo == "Eliminación Gaussiana":
                        x = Eliminacion_Gaussiana(A, b)
                        self.mostrar_resultado(x, metodo)
                    elif metodo == "Pivoteo":
                        A_pivot, b_pivot = pivoteo(A, b)
                        x = Eliminacion_Gaussiana(A_pivot, b_pivot)
                        self.mostrar_resultado(x, metodo)
                elif metodo_tipo == "Iterativo":
                    if metodo == "Gauss-Seidel":
                        tol = float(self.entrada_tol.get())
                        xo_texto = self.entrada_xo.get().strip()
                        xo = np.array(list(map(float, xo_texto.split(','))))
                        x, mensaje = G_seidel(A, b, xo, tol)
                        if x is not None:
                            self.mostrar_resultado(x, metodo)
                        else:
                            messagebox.showinfo("No Convergencia", mensaje)
            except Exception as e:
                messagebox.showerror("Error", f"Error en el método {metodo}: {e}")

    def mostrar_resultado(self, x, metodo):
        resultado = "\n".join([f"x{i+1} = {val:.6f}" for i, val in enumerate(x)])
        messagebox.showinfo(f"Resultado - {metodo}", resultado)

# Crear ventana principal
root = tk.Tk()
app = InterfazSistemasLineales(root)
root.mainloop()
