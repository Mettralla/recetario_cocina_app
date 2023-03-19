from modules.AddIngredient import *
from modules.AddMethod import *
from modules.globalVar import METHOD_LIST, INGREDIENT_LIST, RECIPE_LIST
from modules.Ingredient import Ingredient
from modules.Recipe import Recipe
import csv
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import itertools


class EditRecipe(ttk.Frame):
    def __init__(self, parent, title: str, recipe_id: int) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.id = recipe_id
        self.recipe = self.get_recipe()

        self.name = tk.StringVar()
        self.preparation_time = tk.StringVar()
        self.cooking_time = tk.StringVar()

        parent.title(title)
        parent.geometry('580x650')
        parent.resizable(0, 0)

        # COLUMNS
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=1)
        parent.columnconfigure(4, weight=1)
        parent.columnconfigure(5, weight=1)
        parent.columnconfigure(6, weight=1)

        # ROWS
        parent.rowconfigure(0, weight=1)  # Name
        parent.rowconfigure(1, weight=1)  # Ingredients
        parent.rowconfigure(2, weight=2)  # Ingred list
        parent.rowconfigure(3, weight=1)  # Prep
        parent.rowconfigure(4, weight=2)  # Prep list
        parent.rowconfigure(5, weight=1)  # Time prep
        parent.rowconfigure(6, weight=1)  # time cocc
        parent.rowconfigure(7, weight=1)  # time cocc
        parent.rowconfigure(8, weight=1)  # buttons

        self.create_ui()
        self.set_variables()

    def get_recipe(self) -> dict:
        '''Lee el fichero, identifica la receta a traves del id y la convierte en un diccionario lista para ser mostrada'''
        selected_recipe = {}
        with open(RECIPE_LIST, "r", newline="\n") as csvfile:
            reader = csv.reader(csvfile)
            for recipe in reader:
                try:
                    if int(recipe[0]) == self.id:
                        selected_recipe = {
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
                    else:
                        pass
                except ValueError:
                    pass
        return selected_recipe
        
    
    def create_ui(self) -> None:
        '''Crea la interfaz que usara el usuario para crear la receta'''
        # NOMBRE DE LA RECETA
        ttk.Label(self.parent, text="Nombre:", padding=3).grid(
            row=0, column=1, sticky=tk.EW)
        tk.Entry(self.parent, textvariable=self.name, justify=tk.RIGHT).grid(
            row=0, column=2, columnspan=4, sticky=tk.EW)

        # INGREDIENTES DE LA RECETA
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(
            row=1, column=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar Ingrediente", command=self.new_ingredient).grid(
            row=1, column=2, columnspan=2, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Eliminar Ingrediente", command=self.delete_ingredient).grid(
            row=1, column=4, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_ingredient_tree).grid(
            row=1, column=5, sticky=tk.EW, padx=5)
        # LISTA DE INGREDIENTES
        self.ingredient_list = self.create_ingredient_list()
        self.load_ingredients()

        # # PASOS DE LA RECETA
        ttk.Label(self.parent, text="Preparacion:", padding=3).grid(
            row=3, column=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar Paso", command=self.new_method).grid(
            row=3, column=2, columnspan=2, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Eliminar Paso", command=self.delete_method).grid(
            row=3, column=4, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_method_tree).grid(
            row=3, column=5, sticky=tk.EW, padx=5)
        # LISTA DE PASOS
        self.method_list = self.create_method_list()
        self.load_method_list()

        # TIEMPO DE PREPARACION
        ttk.Label(self.parent, text="Tiempo de Preparacion:", padding=3).grid(
            row=5, column=1, columnspan=3, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.preparation_time, justify=tk.RIGHT).grid(
            row=5, column=3, columnspan=3, sticky=tk.EW)

        # TIEMPO DE COCCION
        ttk.Label(self.parent, text="Tiempo de Cocción:", padding=3).grid(
            row=6, column=1, columnspan=3, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.cooking_time, justify=tk.RIGHT).grid(
            row=6, column=3, columnspan=3, sticky=tk.EW)

        # IMAGEN
        ttk.Label(self.parent, text="Imagen:", padding=3).grid(
            row=7, column=1, columnspan=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar", command=self.add_image).grid(
            row=7, column=3, columnspan=3, sticky=tk.EW)

        # # BOTONERA
        ttk.Button(self.parent, text="Guardar Cambios", command=self.save).grid(
            row=8, column=1, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        ttk.Button(self.parent, text="Cancelar", command=self.parent.destroy).grid(
            row=8, column=3, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)

    def set_variables(self):
        '''Rellena automaticamente los entry con los valores actuales'''
        self.name.set(self.recipe['nombre'])
        self.preparation_time.set(self.recipe['tiempo de preparacion'])
        self.cooking_time.set(self.recipe['tiempo de coccion'])

    #   INGREDIENTES
    def create_ingredient_list(self) -> ttk.Treeview:
        '''Crea el treeview widget que contendra los ingredientes'''
        # Numero de columnas y nombres
        columns = ('Ingredientes', 'Cantidad')
        # Crea el widget
        ingredient_tree = ttk.Treeview(
            self.parent, columns=columns, show='headings', height=5)
        # Lo ubica en la grilla
        ingredient_tree.grid(row=2, column=1, sticky=(
            tk.NSEW), padx=5, columnspan=5)
        # Se agregan los encabezados
        ingredient_tree.heading('Ingredientes', text='Ingredientes')
        ingredient_tree.heading('Cantidad', text='Cantidad')

        return ingredient_tree

    def load_ingredients(self) -> None:
        '''Carga los ingredientes de la lista en el Treeview'''
        ingredients = self.recipe['ingredientes'].split(',')
        amounts = self.recipe['cantidades'].split(',')
        for ingredient, amount in zip(ingredients, amounts):
            self.ingredient_list.insert(
                '', tk.END, values=[ingredient, amount])

    def new_ingredient(self) -> None:
        '''Abre una ventana para agregar un ingrediente'''
        toplevel = tk.Toplevel(self.parent)
        AddIngredient(toplevel).grid()

    def add_ingredient_to_dict(self) -> None:
        '''Agrega la ingrediente al diccionario de la receta que se esta editando'''
        ing = self.recipe['ingredientes'].split(',')
        amts = self.recipe['cantidades'].split(',')
        with open(INGREDIENT_LIST, "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for ingredient in reader:
                new_ingredient = Ingredient(
                    ingredient['nombre'],
                    ingredient['cantidad'],
                    ingredient['medida']
                )
        ing.append(new_ingredient.get_name())
        amts.append(new_ingredient.get_amount())
        self.recipe['ingredientes'] = self.list_to_str(ing)
        self.recipe['cantidades'] = self.list_to_str(amts)

    def refresh_ingredient_tree(self) -> None:
        '''Actualiza la lista de ingredientes'''
        try:
            self.add_ingredient_to_dict()
            self.ingredient_list = self.create_ingredient_list()
            self.load_ingredients()
            self.reset_file(INGREDIENT_LIST, ["nombre", "cantidad", "medida"])
        except UnboundLocalError:
            msg.showerror(message='No realizo ningun cambio', title='Error al actualizar')

    def delete_ingredient(self) -> None:
        '''Elimina el ultimo ingrediente de la lista de ingredientes'''
        try:
            ingredients = self.recipe['ingredientes'].split(',')
            amounts = self.recipe['cantidades'].split(',')
            ingredients.pop(-1)
            amounts.pop(-1)
            self.recipe['ingredientes'] = self.list_to_str(ingredients)
            self.recipe['cantidades'] = self.list_to_str(amounts)
            self.ingredient_list = self.create_ingredient_list()
            self.load_ingredients()
        except IndexError:
            msg.showerror(message='No hay ningun ingrediente en la lista',
            title='Eliminar ingrediente')

    def reset_file(self, route: str, fieldlist: list[str]) -> None:
        '''Elimina los items de las lista temporales dejando solo los encabezados.
            params:
                (str) route: la ruta del csv a resetear
                (list) fieldlist: los encabezados del fichero
        '''
        with open(route, "w", newline="\n") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldlist)
            writer.writeheader()

    def list_to_str(self, f_list:list) -> str:
        '''Transforma la lista de ingredientes en string y la devuelve'''
        str_list = ''
        for item in f_list:
            str_list += item
            if f_list[-1] != item:
                str_list += ','
        return str_list

    # PASOS DE PREPARACION
    def create_method_list(self) -> ttk.Treeview:
        '''Crea el treeview widget que contendra los pasos de preparacion'''
        # Numero de columnas y nombres
        columns = ('Id', 'Paso')
        # Crea el widget
        method_tree = ttk.Treeview(self.parent, columns=columns,
                                   show='headings', height=5)
        # Lo ubica en la grilla
        method_tree.grid(row=4, column=1, sticky=(
            tk.NSEW), padx=5, columnspan=5)
        # Se agregan los encabezados
        method_tree.heading('Id', text='Id')
        method_tree.heading('Paso', text='Paso')

        return method_tree

    def load_method_list(self) -> None:
        '''Carga los ingredientes de la lista en el Treeview'''
        prep_methods = self.recipe['preparacion'].split(',')
        for id, prep_method in enumerate(prep_methods, 1):
            self.method_list.insert(
                '', tk.END, values=[id, prep_method]
            )

    def new_method(self) -> None:
        '''Abre una ventana para agregar paso de preparacion'''
        toplevel = tk.Toplevel(self.parent)
        AddMethod(toplevel).grid()
        
    def add_method_to_dict(self) -> None:
        '''Agrega la ingrediente al diccionario de la receta que se esta editando'''
        prep = self.recipe['preparacion'].split(',')
        with open(METHOD_LIST, "r", newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for prep_method in reader:
                prep.append(prep_method['paso'])
        self.recipe['preparacion'] = self.list_to_str(prep)
        print(prep)
        
    def refresh_method_tree(self) -> None:
        '''Actualiza la lista de preparacion'''
        try:
            self.add_method_to_dict()
            self.method_list = self.create_method_list()
            self.load_method_list()
            self.reset_file(METHOD_LIST, ["id", "paso"])
        except UnboundLocalError:
            msg.showerror(message='No realizo ningun cambio',
                          title='Error al actualizar')

    def delete_method(self) -> None:
        '''Elimina el ultimo elemento de la lista de preparacion'''
        try:
            prep = self.recipe['preparacion'].split(',')
            prep.pop(-1)
            self.recipe['preparacion'] = self.list_to_str(prep)
            self.method_list = self.create_method_list()
            self.load_method_list()
        except IndexError:
            msg.showerror(message='No hay ningun ingrediente en la lista',
                            title='Eliminar ingrediente')

    def add_image(self) -> None:
        '''Guarda la direccion de la imagen a guardar'''
        self.recipe['imagen'] = fd.askopenfilename(
            filetypes=(
                ('jpg files', '*.jpg'), ('All files', '*.*')
            )
        )
        if self.image != None:
            msg.showinfo(
                message='Imagen agregada con exito',
                title='Agregar imagen'
            )
        else:
            msg.showinfo(
                message='Imagen no guardada',
                title='Agregar imagen'
            )
    
    def save(self) -> None:
        '''Toma los datos ingresados en la ventana y los almacena en csv_files'''
        recipes = []
        with open(RECIPE_LIST, "r", newline="\n") as csvfile:
            reader = csv.reader(csvfile)
            for recipe in reader:
                try:
                    if int(recipe[0]) != self.id:
                        selected_recipe = {
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
                        recipes.append(selected_recipe)
                    elif int(recipe[0]) == self.id:
                        edited_recipe = {
                            'id': self.id,
                            'nombre': self.name.get(),
                            'ingredientes': self.recipe['ingredientes'],
                            'cantidades': self.recipe['cantidades'],
                            'preparacion': self.recipe['preparacion'],
                            'tiempo de preparacion': self.preparation_time.get(),
                            'tiempo de coccion': self.cooking_time.get(),
                            'creado': self.recipe['creado'],
                            'imagen': self.recipe['imagen']
                        }
                        recipes.append(edited_recipe)
                    else:
                        pass
                except ValueError:
                    pass
        
        fields = ['id', 'nombre', 'ingredientes', 'cantidades', 'preparacion',
                            'tiempo de preparacion', 'tiempo de coccion', 'creado', 'imagen']
        with open(RECIPE_LIST, 'w', newline='\n') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            for recipe in recipes:
                writer.writerow(
                    {
                        'id': recipe['id'],
                        'nombre': recipe['nombre'],
                        'ingredientes': recipe['ingredientes'],
                        'cantidades': recipe['cantidades'],
                        'preparacion': recipe['preparacion'],
                        'tiempo de preparacion': recipe['tiempo de preparacion'],
                        'tiempo de coccion': recipe['tiempo de coccion'],
                        'creado': recipe['creado'],
                        'imagen': recipe['imagen']
                    }
                )
        self.parent.destroy()