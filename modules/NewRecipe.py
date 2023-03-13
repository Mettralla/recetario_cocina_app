from modules.AddIngredient import *
from modules.AddMethod import *
from modules.globalVar import METHOD_LIST, INGREDIENT_LIST, RECIPE_LIST
from modules.Ingredient import Ingredient
from modules.Recipe import Recipe

class NewRecipe(ttk.Frame):
    def __init__(self, parent, title: str) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent

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
        parent.rowconfigure(5, weight=2)  # Time prep
        parent.rowconfigure(6, weight=2)  # time cocc
        parent.rowconfigure(7, weight=1)  # buttons

        self.create_ui()

    def create_ui(self) -> None:
        '''Crea la interfaz que usara el usuario para crear la receta'''
        self.name = tk.StringVar()
        self.preparation_time = tk.IntVar()
        self.cooking_time = tk.IntVar()

        # NOMBRE DE LA RECETA
        ttk.Label(self.parent, text="Nombre:", padding=3).grid(
            row=0, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.name).grid(
            row=0, column=2, columnspan=4, sticky=tk.EW)

        # INGREDIENTES DE LA RECETA
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(
            row=1, column=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar Ingrediente", command=self.new_ingredient).grid(
            row=1, column=2, columnspan=3, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_ingredient_tree).grid(
            row=1, column=5, sticky=tk.EW, padx=5)
        # LISTA DE INGREDIENTES
        self.ingredient_list = self.create_ingredient_list()
        self.read_ingredient_list()
        
        # PASOS DE LA RECETA
        ttk.Label(self.parent, text="Nombre:", padding=3).grid(
            row=3, column=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar Paso", command=self.new_method).grid(
            row=3, column=2, columnspan=3, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_method_tree).grid(
            row=3, column=5, sticky=tk.EW, padx=5)
        # LISTA DE INGREDIENTES
        self.method_list = self.create_method_list()
        self.read_method_list()
        
        # TIEMPO DE PREPARACION
        ttk.Label(self.parent, text="Tiempo de Preparacion:", padding=3).grid(
            row=5, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.preparation_time, justify= tk.RIGHT).grid(
            row=5, column=2, columnspan=4, sticky=tk.EW)
        
        # TIEMPO DE COCCION
        ttk.Label(self.parent, text="Tiempo de Cocción:", padding=3).grid(
            row=6, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.cooking_time, justify= tk.RIGHT).grid(
            row=6, column=2, columnspan=4, sticky=tk.EW)

        # BOTONERA
        ttk.Button(self.parent, text="Crear", command=self.save).grid(row=7, column=1, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        ttk.Button(self.parent, text="Cancelar", command=self.parent.destroy).grid(row=7, column=3, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)

    # FUNCIONES DE INGREDIENTE
    def create_ingredient_list(self) -> ttk.Treeview:
        '''Crea el treeview widget que contendra los ingredientes'''
        # Numero de columnas y nombres
        columns = ('Ingredientes', 'Cantidad')
        # Crea el widget
        ingredient_tree = ttk.Treeview(self.parent, columns=columns, show='headings', height=5)
        # Lo ubica en la grilla
        ingredient_tree.grid(row=2, column=1, sticky=(tk.NSEW), padx=5, columnspan=5)
        # Se agregan los encabezados
        ingredient_tree.heading('Ingredientes', text='Ingredientes')
        ingredient_tree.heading('Cantidad', text='Cantidad')

        return ingredient_tree
    
    def read_ingredient_list(self) -> None:
        '''Lee el los ingredientes de la lista de ingredientes y los muestra'''
        with open(INGREDIENT_LIST, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for ingredient in reader:
                data = [ingredient["nombre"], ingredient["cantidad"] + ' ' +
                        ingredient["medida"]]
                self.ingredient_list.insert('', tk.END, values=data)

    def new_ingredient(self) -> None: 
        '''Abre una ventana para agregar un ingrediente'''
        toplevel = tk.Toplevel(self.parent)
        AddIngrediente(toplevel).grid()

    def refresh_ingredient_tree(self) -> None:
        '''Actualiza la lista de ingredientes'''
        self.ingredient_list = self.create_ingredient_list()
        self.read_ingredient_list()

    # FUNCIONES DE PASOS
    def create_method_list(self) -> ttk.Treeview:
        '''Crea el treeview widget que contendra los pasos de preparacion'''
        # Numero de columnas y nombres
        columns = ('Id', 'Paso')
        # Crea el widget
        method_tree = ttk.Treeview(self.parent, columns=columns,
                            show='headings', height=5)
        # Lo ubica en la grilla
        method_tree.grid(row=4, column=1, sticky=(tk.NSEW), padx=5, columnspan=5)
        # Se agregan los encabezados
        method_tree.heading('Id', text='Id')
        method_tree.heading('Paso', text='Paso')
        
        return method_tree

    def read_method_list(self) -> None:
        '''Lee los pasos de preparacion de la lista de pasos y los muestra'''
        with open(METHOD_LIST, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for method in reader:
                data = [method["id"], method["paso"]]
                self.method_list.insert('', tk.END, values=data)

    def new_method(self) -> None:
        '''Crea una ventana para agregar un paso a la lista de preparacion'''
        toplevel = tk.Toplevel(self.parent)
        AddMethod(toplevel).grid()

    def refresh_method_tree(self) -> None:
        '''Actualiza la lista de pasos de preparacion'''
        self.method_list = self.create_method_list()
        self.read_method_list()
    
    def get_last_recipe_id(self) -> int:
        '''Obtiene el id del ultimo item de la lista de recetas y lo regresa, si no existe devuelve 0'''
        with open(RECIPE_LIST, 'r') as csvfile:
            reader = csvfile.readlines()
            last_id = reader[-1].split(',')[0]
        if last_id == 'id':
            return 0
        else:
            return int(last_id)
    
    def get_recipe_ingredients(self) -> list[Ingredient]:
        '''Lee el fichero de ingredientes y los convierte en objetos Ingredientes. Devuelve una lista de objetos.'''
        f_ingredients = []
        with open(INGREDIENT_LIST, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for ingredient in reader:
                new_ingredient = Ingredient(
                    ingredient['nombre'], 
                    ingredient['cantidad'], 
                    ingredient['medida']
                )
                f_ingredients.append(new_ingredient)
        self.reset_file(INGREDIENT_LIST, ["nombre", "cantidad", "medida"])
        return f_ingredients
    
    def get_recipe_methods(self) -> list:
        '''Lee la lista de pasos de preparacion y lo formatea para agregar a la receta'''
        f_methods = []
        with open(METHOD_LIST, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for prep_method in reader:
                f_methods.append(prep_method['paso'])
        self.reset_file(METHOD_LIST, ["id", "paso"])
        return f_methods
    
    def get_recipe(self) -> dict[str]:
        '''Toma los valores ingresados y los convierte en un objeto Receta, regresa los datos formateados en un diccionario de strings'''
        new_recipe = Recipe(
            id = self.get_last_recipe_id() + 1,
            name = self.name.get(), 
            ingredients = self.get_recipe_ingredients(),
            preparation = self.get_recipe_methods(),
            preparation_time = self.preparation_time.get(),
            cooking_time = self.cooking_time.get()
        )
        return new_recipe.format_values()
    
    def reset_file(self, route: str, fieldlist: list[str]) -> None:
        '''Elimina los items de las lista temporales dejando solo los encabezados.
            params:
                (str) route: la ruta del csv a resetear
                (list) fieldlist: los encabezados del fichero
        '''
        with open(route, "w", newline="\n") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldlist)
            writer.writeheader()
    
    def save(self) -> None:
        '''Toma los datos ingresados en la ventana y los almacena en csv_files'''
        new_recipe = self.get_recipe()
        fields = ['id', 'nombre', 'ingredientes', 'cantidades', 'preparacion', 'tiempo de preparacion', 'tiempo de coccion', 'creado']
        with open(RECIPE_LIST, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writerow(
                {
                    'id': new_recipe['id'],
                    'nombre': new_recipe['nombre'],
                    'ingredientes': new_recipe['ingredientes'],
                    'cantidades': new_recipe['cantidades'],
                    'preparacion': new_recipe['preparacion'],
                    'tiempo de preparacion': new_recipe['tiempo de preparacion'],
                    'tiempo de coccion': new_recipe['tiempo de coccion'],
                    'creado': new_recipe['creado']
                }
            )
        self.parent.destroy()