import tkinter as tk
from tkinter import ttk
from src.windows.NewRecipe import *
from src.windows.ReadRecipe import ReadRecipe
from src.windows.EditRecipe import EditRecipe
import os
from datetime import datetime
import random
from src.utils.db_utils import DBUtils


class App(ttk.Frame):
    '''La clase representa la ventana principal donde el usuario vera las recetas y podra realizar el CRUD'''
    def __init__(self, parent=None) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.search_option = tk.StringVar()
        self.search_input = tk.StringVar()
        
        self.edited_row = None
        self.edit_flag = False
        
        self.added_row = None
        self.new_flag = False
        
        self.treeview_content = []

        self.db_utils = DBUtils()
        self.db_utils.connect()

        # MAIN WINDOW
        parent.geometry('1280x720')
        parent.title('Kitchen App')
        parent.resizable(0, 0)
        parent.config(bg='#d9d9d9')
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Add the rowheight
        self.style.configure('Treeview', rowheight=30)

        # BUTTONS
        self.set_ui()

        # COLUMNS
        for i in range(5):
            if i == 0:
                parent.columnconfigure(i, weight=4)
            else:
                parent.columnconfigure(i, weight=1)

        # ROWS
        for i in range(6):
            if i == 0:
                parent.rowconfigure(i, weight=1)
            else:
                parent.rowconfigure(i, weight=7)

        self.tree = self.create_tree()
        self.read_data()

    def set_ui(self) -> None:
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
        ttk.Button(self.parent, text="Actualizar", command=self.recover_treeview_data).grid(
            row=5, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        
        ttk.Combobox(self.parent, textvariable=self.search_option, 
            values=['Nombre', 'Etiquetas', 'Tiempo de Preparacion', 'Ingredientes'], justify=tk.RIGHT).grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)
        ttk.Entry(self.parent, textvariable=self.search_input, justify=tk.RIGHT).grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
        ttk.Button(self.parent, text="Buscar", command=self.search).grid(
            row=0, column=3, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Reset", command=self.recover_treeview_data).grid(
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
        tree.column(2, anchor=tk.CENTER, stretch=tk.NO, width=350)
        #TIEMPO DE PREPARACION
        tree.heading('Tiempo de Preparacion', text='Tiempo de Preparacion')
        tree.column(3, anchor=tk.CENTER, stretch=tk.NO, width=140)
        #TIEMPO DE COCCION
        tree.heading('Tiempo de Coccion', text='Tiempo de Coccion')
        tree.column(4, anchor=tk.CENTER, stretch=tk.NO, width=140)
        #CREADO EN
        tree.heading('Creado', text='Creado')
        tree.column(5, anchor=tk.CENTER, stretch=tk.NO, width=140)

        # AGREGAR SCROLLBAR
        scrollbar = ttk.Scrollbar(
            self.parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=10, rowspan=5)

        return tree

    def read_data(self):
        self.recipe_list = self.db_utils.read_recipes()
        for recipe in self.recipe_list:
            data = [recipe[0], recipe[1], recipe[5], f'{recipe[2]} min', f'{recipe[3]} min', recipe[4]]
            self.tree.insert('', tk.END, values= data)

    #CRUD
    def new_recipe(self) -> None:
        '''Abre una nueva ventana para agregar una receta'''
        try:
            toplevel = tk.Toplevel(self.parent)
            new_recipe_window = NewRecipe(toplevel, 'Agregar Receta', self).grid()
            toplevel.wait_window(new_recipe_window)
            if self.new_flag:
                ingredients = ''
                for ingredient_details in self.added_row['ingredients']:
                    ingredients += f'{ingredient_details[1]},'
                new_value = (
                    self.added_row['id'],
                    self.added_row['name'],
                    ingredients[:-1],
                    f"{self.added_row['prep_time']} min",
                    f"{self.added_row['cook_time']} min",
                    self.added_row['created_at']
                )
                self.tree.insert('', tk.END, values=new_value)
                self.new_flag = False
        except Exception as e:
            msg.showerror(message=f'Error: {e}', title='Nueva Receta', parent = self.parent)

    def edit_recipe(self) -> None:
        '''Abre una ventana para agregar una receta'''
        try:
            item = self.get_recipe_id()
            id = item[0]
            row = item[1]
            toplevel = tk.Toplevel(self.parent)
            edit_window = EditRecipe(toplevel, 'Editar Receta', id, self).grid()
            toplevel.wait_window(edit_window)
            if self.edit_flag:
                new_value = (
                    id, 
                    self.edited_row[0], 
                    self.edited_row[1], 
                    f'{self.edited_row[2]} min', 
                    f'{self.edited_row[3]} min', 
                    self.tree.item(row)['values'][5]
                )
                self.tree.item(row, values=new_value)
                self.edit_flag = False
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Editar Receta', parent = self.parent)

    def delete_recipe(self) -> None:
        '''Elimina una receta del fichero csv'''
        try:
            select_item = self.get_recipe_id()
            self.db_utils.delete_recipe(select_item[0])
            self.refresh_recipe_tree()
            msg.showinfo(message='Receta eliminada con exito, actualice la lista', title='Eliminar Receta', parent = self.parent)
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Eliminar Receta', parent=self.parent)
    
    def read_recipe(self) -> None:
        '''Abre una nueva ventana para leer una receta'''
        try: 
            item = self.get_recipe_id()
            id = item[0]
            toplevel = tk.Toplevel(self.parent)
            ReadRecipe(toplevel, 'Leer Receta', id).grid()
        except IndexError:
            msg.showerror(
                message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Ver Receta', parent=self.parent)

    def refresh_recipe_tree(self) -> None:
        '''Actualiza la lista de recetas'''
        self.tree.delete(*self.tree.get_children())
        self.tree = self.create_tree()
        self.read_data()

    def recover_treeview_data(self):
        if len(self.treeview_content) == 0:
            msg.showinfo(
                message='El recetario esta al dia', title='Recetas', parent=self.parent)
        else:
            self.tree.delete(*self.tree.get_children())
            for recipe in self.treeview_content:
                self.tree.insert('', tk.END, values=recipe)
            self.treeview_content = []

    def save_treeview(self):
        for item in self.tree.get_children():
            recipe = self.tree.item(item, "values")
            self.treeview_content.append(recipe)

    def get_recipe_id(self) -> int:
        '''Guarda el id del item seleccionado al presionar un boton'''
        select_item = self.tree.focus()
        return self.tree.item(select_item)['values'][0], select_item

    def search(self) -> None:
        '''Recibe los datos ingresados en entry y lo redirige a la busqueda adecuada e inserta los valores en treeview.'''
        option = self.search_option.get()
        search_in = self.search_input.get()
        if option == 'Nombre':
            self.search_by_name(search_in)
        elif option == 'Etiquetas':
            self.search_by_tags(search_in)
        elif option == 'Tiempo de Preparacion':
            self.search_by_prep_time(search_in)
        elif option == 'Ingredientes':
            self.search_by_ingredients(search_in)
        else:
            msg.showerror(title='Buscar', message='Error! Escoja una opcion valida')

    def read_search_data(self, recipes) -> None:
        '''Lee el fichero csv e inserta los datos en el treeview'''
        if len(recipes) != 0:
            self.tree = self.create_tree()
            for recipe in recipes:
                data = [recipe[0], recipe[1], recipe[5], f'{recipe[2]} min', f'{recipe[3]} min', recipe[4]]
                self.tree.insert('', tk.END, values=data)
        else:
            msg.showwarning(
                title='Buscar', message='No se ha encontrado coincidencias', parent=self.parent)

    def search_by_name(self, name: str) -> None:
        '''Busca las recetas por nombre.
            params:
                (str) name: nombre buscado.'''
        self.save_treeview()
        found_recipes = self.db_utils.search_by_name(name)
        self.read_search_data(found_recipes)

    def search_by_tags(self, tags: str) -> None:
        '''Busca las recetas que tengan las etiquetas buscadas.
            params:
                (str) tags: las etiquetas buscados separados por coma.'''
        self.save_treeview()
        found_recipes  = self.db_utils.search_by_tags(tags)
        self.read_search_data(found_recipes)

    def search_by_prep_time(self, prep_time: str) -> None:
        '''Busca las recetas que coincidan con el tiempo de preparacion deseado.
            params:
                (str) prep_time: el tiempo de preparacion buscado.'''
        self.save_treeview()
        found_recipes = self.db_utils.search_by_prep_time(prep_time)
        self.read_search_data(found_recipes)

    def search_by_ingredients(self, ingredients: str) -> None:
        '''Busca las recetas que contengan los ingredientes ingresados.
            params:
                (str) ingredients: los ingredientes buscados separados por coma.'''
        self.save_treeview()
        found_recipes = self.db_utils.search_by_ingredient(ingredients)
        self.read_search_data(found_recipes)

    def __del__(self):
        self.db_utils.disconnect()


root = tk.Tk()
App(root).grid()
root.mainloop()
