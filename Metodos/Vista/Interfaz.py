import importlib
import tkinter as tk
from tkinter import messagebox
from tkinter import Menu

class InterfazPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis Númerico")
        self.root.geometry("400x600")  # Tamaño de la ventana principal
        self.root.configure(bg="#2C3E50")  # Fondo de la ventana principal

        self.crear_menu()

        titulo = tk.Label(
            root,
            text="Métodos Numéricos",
            font=("Helvetica", 24, "bold"),
            fg="#ECF0F1",
            bg="#2C3E50"
        )
        titulo.pack(pady=20)

        opciones = [
            ("Ceros de Funciones", "Metodos.Modelo.Ceros", "InterfazCeros"),
            ("Ecuaciones Diferenciales", "Metodos.Modelo.Ecuaciones", "InterfazEcuaciones"),
            ("Interpolación y Ajuste de Curva", "Metodos.Modelo.Interpolacion", "InterfazInterpolacionAjuste"),
            ("Serie de Taylor", "Metodos.Modelo.SerieTaylor", "InterfazSerieTaylor"),
            ("Sistemas de Ecuaciones Lineales", "Metodos.Modelo.Sistemas_ecuaciones_lineales", "InterfazSistemasLineales")
        ]

        for i, (opcion, modulo, clase) in enumerate(opciones):
            boton = tk.Button(
                root,
                text=opcion,
                command=lambda m=modulo, c=clase: self.abrir_interfaz(m, c),
                width=30,
                height=2,
                padx=10,
                pady=10,
                relief=tk.FLAT,
                font=("Helvetica", 14),
                bg="#34495E",
                fg="#ECF0F1",
                activebackground="#1ABC9C",
                activeforeground="#2C3E50",
                borderwidth=2,
                highlightbackground="#2C3E50",
                highlightcolor="#1ABC9C",
                highlightthickness=2
            )
            boton.bind("<Enter>", self.on_enter)
            boton.bind("<Leave>", self.on_leave)
            boton.pack(pady=10)

        # Barra
        self.status_bar = tk.Label(root, text="Bienvenido", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#2C3E50", fg="#ECF0F1")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_enter(self, e):
        e.widget['bg'] = '#1ABC9C'
        e.widget['fg'] = '#2C3E50'

    def on_leave(self, e):
        e.widget['bg'] = '#34495E'
        e.widget['fg'] = '#ECF0F1'

    def abrir_interfaz(self, modulo, clase):
        try:
            mod = importlib.import_module(modulo)
            clase_interfaz = getattr(mod, clase)
            ventana = tk.Toplevel(self.root)
            ventana.configure(bg="#2C3E50")
            clase_interfaz(ventana)
            self.status_bar.config(text=f"Abierta interfaz de {modulo.split('.')[-1]}")
        except ImportError as e:
            messagebox.showerror("Error", f"Error al importar el módulo: {modulo}\n{e}")
            self.status_bar.config(text="Error al importar módulo")
        except AttributeError as e:
            messagebox.showerror("Error", f"Error al acceder a la clase: {clase}\n{e}")
            self.status_bar.config(text="Error al acceder a la clase")

    def crear_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Menú Archivo
        archivo_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        # Menú Ayuda
        ayuda_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)

    def mostrar_acerca_de(self):
        messagebox.showinfo("Acerca de", "Aplicación de Análisis Numérico\nAutor: Laura López y Juan Pablo Ramirez")

# Crear ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazPrincipal(root)
    root.mainloop()
