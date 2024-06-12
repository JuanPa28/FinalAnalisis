# Archivo: Metodos/Vista/Interfaz.py

import tkinter as tk
from tkinter import messagebox
import importlib

class InterfazPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("400x300")  # Tamaño de la ventana principal

        # Lista de opciones disponibles
        opciones = [
            ("Ceros de Funciones", "Metodos.Modelo.Ceros", "InterfazCeros"),
            ("Ecuaciones Diferenciales", "Metodos.Modelo.Ecuaciones", "InterfazEcuaciones"),
            ("Interpolación y Ajuste de Curva", "Metodos.Modelo.Interpolacion", "InterfazInterpolacionAjuste"),
            ("Serie de Taylor", "Metodos.Modelo.SerieTaylor", "InterfazSerieTaylor"),
            ("Sistemas de Ecuaciones Lineales", "Metodos.Modelo.Sistemas_ecuaciones_lineales", "InterfazSistemasLineales")
        ]

        # Crear botones para cada opción
        for i, (opcion, modulo, clase) in enumerate(opciones):
            boton = tk.Button(
                root,
                text=opcion,
                command=lambda m=modulo, c=clase: self.abrir_interfaz(m, c),
                width=30,  # Ancho del botón
                height=2,  # Alto del botón
                padx=10,  # Padding en x
                pady=10,  # Padding en y
                relief=tk.RAISED,  # Estilo de relieve del botón
                font=("Helvetica", 12)  # Fuente y tamaño del texto
            )
            boton.pack(pady=10)  # Empaquetar el botón con espacio vertical entre ellos

    def abrir_interfaz(self, modulo, clase):
        mod = importlib.import_module(modulo)
        clase_interfaz = getattr(mod, clase)
        ventana = tk.Toplevel(self.root)
        clase_interfaz(ventana)

# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazPrincipal(root)
    root.mainloop()
