import tkinter as tk
from tkinter import ttk
import csv
from modules.globalVar import RECIPE_LIST
from modules.NewRecipe import *

class App(ttk.Frame):
    '''La clase representa la ventana principal donde el usuario vera las recetas y podra realizar el CRUD'''
    def __init__(self, parent=None) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent

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
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=1)
        parent.columnconfigure(4, weight=1)
        # ROWS
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1)
        parent.rowconfigure(2, weight=12)
        


    def set_ui(self) -> ttk.Button:
        '''Crea los botones y los ubica en la grilla'''

        # BUTTONS - CRUD + REFRESH
        # CREAR NUEVA RECETA
        ttk.Button(self.parent, text="Nueva", command=self.new_recipe).grid(
            row=0, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # EDITAR RECETA EXISTENTE
        ttk.Button(self.parent, text="Editar", command=self.edit_recipe).grid(
            row=0, column=1, padx=10, pady=5, sticky=(tk.NSEW))
        # VER UNA RECETA
        ttk.Button(self.parent, text="Ver", command=self.read_recipe).grid(
            row=0, column=2, padx=10, pady=5, sticky=(tk.NSEW))
        # ELIMINAR UNA RECETA
        ttk.Button(self.parent, text="Eliminar", command=self.delete_recipe).grid(
            row=0, column=3, padx=10, pady=5, sticky=(tk.NSEW))
        # ACTUALIZAR TREEVIEW
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_recipe_tree).grid(
            row=0, column=4, padx=10, pady=5, sticky=(tk.NSEW))


    def create_tree(self) -> ttk.Treeview:
        '''Crea el treeview widget que contendra las recipes'''

        # NUMERO DE COLUMNAS Y NOMBRES
        columns = ('ID', 'Nombre', 'Ingredientes', 'Tiempo de Preparacion', 'Tiempo de Coccion', 'Creado')
        # CREA EL WIDGET
        tree = ttk.Treeview(self.parent, columns=columns, show='headings')
        # INSERTARLO EN LA GRILLA
        tree.grid(row=2, column=0, sticky=(tk.NSEW), pady=10, padx=5, columnspan=5)
        # INSERTAR EL ENCABEZADO
        tree.heading('ID', text='ID')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Ingredientes', text='Ingredientes')
        # tree.heading('Preparacion', text='Preparacion')
        tree.heading('Tiempo de Preparacion', text='Tiempo de Preparacion')
        tree.heading('Tiempo de Coccion', text='Tiempo de Coccion')
        tree.heading('Creado', text='Creado')

        # AGREGAR SCROLLBAR
        scrollbar = ttk.Scrollbar(
            self.parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=2, column=5, sticky=tk.NS, pady=10)

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
            select_item = self.get_recipe_id()
            print(self.tree.item(select_item)['values'][0])
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Editar Receta')
        
    def delete_recipe(self) -> None:
        '''Elimina una receta del fichero csv'''
        try:
            select_item = self.get_recipe_id()
            recipes = []
            fieldlist = ["id", "nombre", "ingredientes", "cantidades", "preparacion", "tiempo de preparacion", "tiempo de coccion", "creado", "imagen"]
            with open(RECIPE_LIST, "r", newline="\n") as csvfile:
                reader = csv.reader(csvfile)
                for recipe in reader:
                    try:
                        if int(recipe[0]) != int(select_item):
                            recipes.append(recipe)
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
                            'imagen': recipe[8]
                        }
                    )
            msg.showinfo(message='Receta eliminada con exito, actualice la lista', title='Eliminar Receta')
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Eliminar Receta')
    
    def read_recipe(self) -> None:
        pass
        
    def refresh_recipe_tree(self) -> None:
        '''Actualiza la lista de recetas'''
        self.tree = self.create_tree()
        self.read_data()

    def get_recipe_id(self) -> str:
        '''Guarda el id del item seleccionado al presionar un boton'''
        select_item = self.tree.focus()
        return self.tree.item(select_item)['values'][0]

root = tk.Tk()
App(root).grid()
root.mainloop()
