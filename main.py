import tkinter as tk
from tkinter import ttk
import csv
from modules.globalVar import RECIPE_LIST
from modules.NewRecipe import *
from modules.ReadRecipe import ReadRecipe
from modules.EditRecipe import EditRecipe
import os

class App(ttk.Frame):
    '''La clase representa la ventana principal donde el usuario vera las recetas y podra realizar el CRUD'''
    def __init__(self, parent=None) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.search_option = tk.StringVar()
        self.search_input = tk.StringVar()

        # MAIN WINDOW
        parent.geometry('1280x720')
        parent.title('Kitchen App')
        parent.resizable(0, 0)

        # BUTTONS
        self.set_ui()

        # DATA LIST
        self.tree = self.create_tree()
        self.read_data()

        # GRID
        # COLUMNS
        parent.columnconfigure(0, weight=4)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=1)
        parent.columnconfigure(4, weight=1)
        # ROWS
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=6)
        parent.rowconfigure(2, weight=6)
        parent.rowconfigure(3, weight=6)
        parent.rowconfigure(4, weight=6)
        parent.rowconfigure(5, weight=6)
        


    def set_ui(self) -> ttk.Button:
        '''Crea los botones y los ubica en la grilla'''

        # BUTTONS - CRUD + REFRESH
        # CREAR NUEVA RECETA
        ttk.Button(self.parent, text="Nueva", command=self.new_recipe).grid(
            row=1, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # EDITAR RECETA EXISTENTE
        ttk.Button(self.parent, text="Editar", command=self.edit_recipe).grid(
            row=2, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # VER UNA RECETA
        ttk.Button(self.parent, text="Ver", command=self.read_recipe).grid(
            row=3, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # ELIMINAR UNA RECETA
        ttk.Button(self.parent, text="Eliminar", command=self.delete_recipe).grid(
            row=4, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # ACTUALIZAR TREEVIEW
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_recipe_tree).grid(
            row=5, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        
        ttk.Combobox(self.parent, textvariable=self.search_option, 
            values=['Nombre', 'Etiquetas', 'Tiempo de Preparacion', 'Ingredientes']).grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)
        ttk.Entry(self.parent, textvariable=self.search_input, justify=tk.RIGHT).grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
        ttk.Button(self.parent, text="Buscar", command=self.refresh_recipe_tree).grid(
            row=0, column=3, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_recipe_tree).grid(
            row=0, column=4, padx=10, pady=5, sticky=(tk.NSEW))


    def create_tree(self) -> ttk.Treeview:
        '''Crea el treeview widget que contendra las recipes'''

        # NUMERO DE COLUMNAS Y NOMBRES
        columns = ('ID', 'Nombre', 'Ingredientes', 'Tiempo de Preparacion', 'Tiempo de Coccion', 'Creado')
        # CREA EL WIDGET
        tree = ttk.Treeview(self.parent, columns=columns, show='headings')
        # INSERTARLO EN LA GRILLA
        tree.grid(row=1, column=1, sticky=(tk.NSEW), pady=10, padx=5, columnspan=4, rowspan=5)
        # INSERTAR EL ENCABEZADO
        #ID
        tree.heading('ID', text='ID')
        tree.column(0, anchor=tk.CENTER, stretch=tk.NO, width=40)
        #NOMBRE
        tree.heading('Nombre', text='Nombre')
        tree.column(1, anchor=tk.CENTER)
        #INGREDIENTES
        tree.heading('Ingredientes', text='Ingredientes')
        tree.column(2, anchor=tk.CENTER)
        #TIEMPO DE PREPARACION
        tree.heading('Tiempo de Preparacion', text='Tiempo de Preparacion')
        tree.column(3, anchor=tk.CENTER)
        #TIEMPO DE COCCION
        tree.heading('Tiempo de Coccion', text='Tiempo de Coccion')
        tree.column(4, anchor=tk.CENTER)
        #CREADO EN
        tree.heading('Creado', text='Creado')
        tree.column(5, anchor=tk.CENTER)

        # AGREGAR SCROLLBAR
        scrollbar = ttk.Scrollbar(
            self.parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=10, rowspan=5)

        return tree


    def read_data(self) -> None:
        '''Lee el fichero csv e inserta los datos en el treeview'''
        with open(RECIPE_LIST, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for recipe in reader:
                data = [recipe['id'],recipe["nombre"], recipe["ingredientes"], recipe["tiempo de preparacion"], recipe["tiempo de coccion"], recipe["creado"]]
                self.tree.insert('', tk.END, values= data)

    #CRUD
    def new_recipe(self) -> None:
        '''Abre una nueva ventana para agregar una receta'''
        toplevel = tk.Toplevel(self.parent)
        NewRecipe(toplevel, 'Agregar Receta').grid()
        
    def edit_recipe(self) -> None:
        '''Abre una ventana para agregar una receta'''
        try:
            id = self.get_recipe_id()
            toplevel = tk.Toplevel(self.parent)
            EditRecipe(toplevel, 'Editar Receta', id)
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Editar Receta', parent = self.parent)
        
    def delete_recipe(self) -> None:
        '''Elimina una receta del fichero csv'''
        try:
            select_item = self.get_recipe_id()
            recipes = []
            fieldlist = ["id", "nombre", "ingredientes", "cantidades", "preparacion", "tiempo de preparacion", "tiempo de coccion", "creado", "imagen", "etiquetas", "favorito"]
            with open(RECIPE_LIST, "r", newline="\n") as csvfile:
                reader = csv.reader(csvfile)
                for recipe in reader:
                    try:
                        if int(recipe[0]) != int(select_item):
                            recipes.append(recipe)
                        elif int(recipe[0]) == int(select_item):
                            if recipe[8] != 'None':
                                os.remove(recipe[8])
                    except ValueError:
                        pass
            with open(RECIPE_LIST, "w", newline="\n") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldlist)
                writer.writeheader()
                for recipe in recipes:
                    writer.writerow(
                        {
                            'id': recipe[0],
                            'nombre': recipe[1],
                            'ingredientes': recipe[2],
                            'cantidades': recipe[3],
                            'preparacion': recipe[4],
                            'tiempo de preparacion': recipe[5],
                            'tiempo de coccion': recipe[6],
                            'creado': recipe[7],
                            'imagen': recipe[8],
                            'etiquetas': recipe[9],
                            'favorito': recipe[10]
                        }
                    )
            msg.showinfo(message='Receta eliminada con exito, actualice la lista', title='Eliminar Receta', parent = self.parent)
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Eliminar Receta', parent=self.parent)
    
    def read_recipe(self) -> None:
        '''Abre una nueva ventana para leer una receta'''
        try: 
            id = self.get_recipe_id()
            toplevel = tk.Toplevel(self.parent)
            ReadRecipe(toplevel, 'Leer Receta', id).grid()
        except IndexError:
            msg.showerror(
                message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Ver Receta', parent=self.parent)
        
    def refresh_recipe_tree(self) -> None:
        '''Actualiza la lista de recetas'''
        self.tree = self.create_tree()
        self.read_data()

    def get_recipe_id(self) -> int:
        '''Guarda el id del item seleccionado al presionar un boton'''
        select_item = self.tree.focus()
        return self.tree.item(select_item)['values'][0]

root = tk.Tk()
App(root).grid()
root.mainloop()
