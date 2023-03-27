import tkinter as tk
from tkinter import ttk
import csv
from modules.globalVar import RECIPE_LIST, RECIPE_OF_THE_DAY
from modules.NewRecipe import *
from modules.ReadRecipe import ReadRecipe
from modules.EditRecipe import EditRecipe
import os
from datetime import datetime
import random

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
        parent.config(bg='#d9d9d9')
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Add the rowheight
        self.style.configure('Treeview', rowheight=30)

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
        parent.rowconfigure(1, weight=7)
        parent.rowconfigure(2, weight=7)
        parent.rowconfigure(3, weight=7)
        parent.rowconfigure(4, weight=7)
        parent.rowconfigure(5, weight=7)

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
            values=['Nombre', 'Etiquetas', 'Tiempo de Preparacion', 'Ingredientes'], justify=tk.RIGHT).grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)
        ttk.Entry(self.parent, textvariable=self.search_input, justify=tk.RIGHT).grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
        ttk.Button(self.parent, text="Buscar", command=self.search).grid(
            row=0, column=3, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Reset", command=self.refresh_recipe_tree).grid(
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


    def read_data(self) -> None:
        '''Lee el fichero csv e inserta los datos en el treeview'''
        if self.new_day():
            self.save_recipe_otd()
        recipe_otd = self.get_recipe_otd()
        recipe_otd_data = self.read_recipe_otd()
        with open(RECIPE_LIST, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            self.tree.insert('', tk.END, values=recipe_otd, tags="recipe_otd")
            self.tree.tag_configure("recipe_otd", foreground="white", background="black")
            for recipe in reader:
                if recipe['id'] != recipe_otd_data[0]:
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

    def search(self) -> None:
        '''Recibe los datos ingresados en entry y lo redirige a la busqueda adecuada e inserta los valores en treeview.'''
        option = self.search_option.get()
        search_in = self.search_input.get()
        fieldlist = ["id", "nombre", "ingredientes", "cantidades", "preparacion",
                     "tiempo de preparacion", "tiempo de coccion", "creado", "imagen", "etiquetas", "favorito"]
        if option == 'Nombre':
            self.search_by_name(fieldlist, search_in)
        elif option == 'Etiquetas':
            self.search_by_tags(fieldlist, search_in)
        elif option == 'Tiempo de Preparacion':
            self.search_by_prep_time(fieldlist, search_in)
        elif option == 'Ingredientes':
            self.search_by_ingredients(fieldlist, search_in)
        else:
            msg.showerror(title='Buscar', message='Error! Escoja una opcion valida')

    def read_search_data(self, recipes: list[dict]) -> None:
        '''Lee el fichero csv e inserta los datos en el treeview'''
        if len(recipes) != 0:
            self.tree = self.create_tree()
            for recipe in recipes:
                data = [recipe['id'], recipe["nombre"], recipe["ingredientes"],
                        recipe["tiempo de preparacion"], recipe["tiempo de coccion"], recipe["creado"]]
                self.tree.insert('', tk.END, values=data)
        else:
            msg.showwarning(
                title='Buscar', message='No se ha encontrado coincidencias', parent=self.parent)

            
    def search_by_name(self, fieldlist: list[str], name: str) -> None:
        '''Busca las recetas por nombre.
            params:
                (list[str]): fieldlist: keys del diccionario Receta.
                (str) name: nombre buscado.'''
        found_recipes = []
        with open(RECIPE_LIST,  "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldlist)
            for recipe in reader:
                if recipe['nombre'].lower() == name.lower():
                    found_recipes.append(recipe)
        self.read_search_data(found_recipes)

    def search_by_tags(self, fieldlist: list[str], tags: str) -> None:
        '''Busca las recetas que tengan las etiquetas buscadas.
            params:
                (list[str]): fieldlist: keys del diccionario Receta.
                (str) tags: las etiquetas buscados separados por coma.'''
        found_recipes = []
        with open(RECIPE_LIST,  "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldlist)
            for recipe in reader:
                for tag in recipe['etiquetas'].split(','):
                    if tag.strip() in tags.split(',') and recipe not in found_recipes:
                        found_recipes.append(recipe)
        self.read_search_data(found_recipes)

    def search_by_prep_time(self, fieldlist: list[str], prep_time: str) -> None:
        '''Busca las recetas que coincidan con el tiempo de preparacion deseado.
            params:
                (list[str]): fieldlist: keys del diccionario Receta.
                (str) prep_time: el tiempo de preparacion buscado.'''
        found_recipes = []
        with open(RECIPE_LIST,  "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldlist)
            for recipe in reader:
                if recipe['tiempo de preparacion'].split(' ')[0] == prep_time.split(' ')[0]:
                    found_recipes.append(recipe)
        self.read_search_data(found_recipes)

    def search_by_ingredients(self, fieldlist: list[str], ingredients: str) -> None:
        '''Busca las recetas que contengan los ingredientes ingresados.
            params:
                (list[str]): fieldlist: keys del diccionario Receta.
                (str) ingredients: los ingredientes buscados separados por coma.'''
        found_recipes = []
        with open(RECIPE_LIST,  "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldlist)
            for recipe in reader:
                for searched_ingredient in ingredients.split(','):
                    if searched_ingredient.strip() in recipe['ingredientes'].split(',') and recipe not in found_recipes:
                        found_recipes.append(recipe)
        self.read_search_data(found_recipes)

    def new_recipe_otd_id(self) -> int:
        '''Lee las recetas las ingresa a una lista y escoge una al azar y devuelve el id'''
        fieldlist = ["id", "nombre", "ingredientes", "cantidades", "preparacion",
                     "tiempo de preparacion", "tiempo de coccion", "creado", "imagen", "etiquetas", "favorito"]
        ids = []
        with open(RECIPE_LIST,  "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldlist)
            for recipe in reader:
                if recipe['id'] != 'id':
                    ids.append(recipe['id'])
        rand_recipe = random.randint(0, len(ids) - 1)
        return ids[rand_recipe]

    def save_recipe_otd(self) -> None:
        '''Escribe la receta del dia en el fichero, cuyo parametros es el id y la fecha'''
        fieldlist = ["id", "dia"]
        with open(RECIPE_OF_THE_DAY, "w", newline="\n") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldlist)
            writer.writeheader()
            writer.writerow({'id': self.new_recipe_otd_id(), 'dia': datetime.now().strftime("%Y,%m,%d")})

    def read_recipe_otd(self) -> list:
        '''Lee el fichero de la receta del dia y devuelve una lista con los parametros:
            (int) id: el id de la receta del dia
            (str) dia: fecha en formato YYYY,MM,DD'''
        recipe_otd = []
        fieldlist = ["id", "dia"]
        with open(RECIPE_OF_THE_DAY,  "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldlist)
            for recipe in reader:
                if recipe['id'] != 'id':
                    recipe_otd.append(recipe['id'])
                    recipe_otd.append(recipe['dia'])
        return recipe_otd

    def count_recipes(self) -> int:
        '''Cuenta la cantidad de recetas en la lista de recetas'''
        count = 0
        with open(RECIPE_LIST,  "r", newline="\n") as csvfile:
            reader = csv.reader(csvfile)
            for _ in reader:
                count += 1
        return count
    
    def new_day(self):
        '''Chequea si han pasado un dia desde que se asigno la receta del dia'''
        recipe_otd = self.read_recipe_otd()
        rotd_to_list = recipe_otd[1].split(',')
        rotd_day = datetime(int(rotd_to_list[0]), int(rotd_to_list[1]), int(rotd_to_list[2]))
        delta = datetime.now() - rotd_day
        return True if delta.days != 0 else False

    def get_recipe_otd(self) -> list[str]:
        '''Recibe el id de la receta del dia, busca el id en la lista y devuelve una lista formateada para ser agregada al Treeview'''
        recipe_otd_data = self.read_recipe_otd()
        with open(RECIPE_LIST, "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for recipe in reader:
                try:
                    if recipe['id'] == recipe_otd_data[0]:
                        return [recipe['id'], recipe["nombre"] + " [RECETA DEL DIA]", recipe["ingredientes"], recipe["tiempo de preparacion"], recipe["tiempo de coccion"], recipe["creado"]]
                except ValueError:
                    pass

root = tk.Tk()
App(root).grid()
root.mainloop()
