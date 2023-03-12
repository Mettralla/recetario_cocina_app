import tkinter as tk
from tkinter import ttk
import csv
from modules.CreateRecipe import *

class App(ttk.Frame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent

        # MAIN WINDOW
        parent.geometry('1024x720')
        parent.title('Kitchen App')
        parent.resizable(0, 0)

        # BUTTONS
        self.set_ui()

        # DATA LIST
        self.tree = self.create_tree()
        self.read_data()

        # GRID
        # COLUMNS
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=1)
        parent.columnconfigure(4, weight=1)
        # ROWS
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1)
        parent.rowconfigure(2, weight=12)
        


    def set_ui(self) -> None:
        # BUTTONS
        ttk.Button(self.parent, text="Nueva", command=self.new_recipe).grid(
            row=0, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Editar", command=self.new_recipe).grid(
            row=0, column=1, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Ver", command=self.new_recipe).grid(
            row=0, column=2, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Eliminar", command=self.new_recipe).grid(
            row=0, column=3, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Actualizar", command=self.new_recipe).grid(
            row=0, column=4, padx=10, pady=5, sticky=(tk.NSEW))


    def create_tree(self) -> None:
        '''Crea el treeview widget que contendra las recipes'''

        # Numero de columnas y nombres
        columns = ('Id', 'Nombre', 'Tiempo de Preparacion')
        # Crea el widget
        tree = ttk.Treeview(self.parent, columns=columns, show='headings')
        # Lo ubica en la grilla
        tree.grid(row=2, column=0, sticky=(tk.NSEW), pady=10, padx=5, columnspan=5)
        # Se agregan los encabezados
        tree.heading('Id', text='Id')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Tiempo de Preparacion', text='Tiempo de Preparacion')

        # Agregar scrollbar
        scrollbar = ttk.Scrollbar(
            self.parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=5, sticky=tk.NS, pady=10)

        return tree


    def read_data(self) -> None:
        '''Lee el fichero csv e inserta los datos en el treeview'''
        with open("csv_files/recipes.csv", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for recipe in reader:
                data = [recipe["id"], recipe["nombre"], recipe["tiempo de preparacion"]]
                self.tree.insert('', tk.END, values= data)


    def new_recipe(self) -> None:
        '''Abre una nueva ventana para agregar una receta'''
        toplevel = tk.Toplevel(self.parent)
        CrearReceta(toplevel, 'Agregar Receta').grid()


root = tk.Tk()
App(root).grid()
root.mainloop()
