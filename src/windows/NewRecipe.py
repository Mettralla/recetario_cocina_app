from src.windows.AddIngredient import *
from src.windows.AddMethod import *
from modules.globalVar import METHOD_LIST, INGREDIENT_LIST, RECIPE_LIST
from src.windows.IBaseWindow import *
from src.Ingredient import Ingredient
from src.Recipe import Recipe
from tkinter import filedialog as fd
from tkinter import messagebox as msg

class NewRecipe(ttk.Frame, IBaseWindow):
    def __init__(self, parent, title: str) -> None:
        ttk.Frame.__init__(self, parent, padding=(20))
        IBaseWindow.__init__(self, parent, title)

        self.name = tk.StringVar()
        self.preparation_time = tk.IntVar()
        self.cooking_time = tk.IntVar()
        self.tags = tk.StringVar()
        self.favorite = tk.StringVar()
        self.image = None

        # AGREGAR LOS BOTONES
        parent.rowconfigure(8, weight=1)  # buttons

        self.create_ui()

    def create_ui(self) -> None:
        '''Crea la interfaz que usara el usuario para crear la receta'''
        # IMAGEN
        ttk.Label(self.parent, text="Imagen:", padding=3).grid(
            row=7, column=1, columnspan=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar", command=self.add_image).grid(
            row=7, column=2, columnspan=4, sticky=tk.EW)

        self.base_ui_config('Crear')

    def load_ingredients(self) -> None:
        '''Lee el los ingredientes de la lista de ingredientes y los muestra'''
        with open(INGREDIENT_LIST, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for ingredient in reader:
                data = [ingredient["cantidad"] + ' ' +
                        ingredient["medida"], ingredient["nombre"]]
                self.ingredient_list.insert('', tk.END, values=data)

    def new_ingredient(self) -> None: 
        '''Abre una ventana para agregar un ingrediente'''
        toplevel = tk.Toplevel(self.parent)
        AddIngredient(toplevel).grid()

    def refresh_ingredient_tree(self) -> None:
        '''Actualiza la lista de ingredientes'''
        self.ingredient_list = self.create_treeview(2, 1, 1, ('Cantidad', 'Ingredientes'))
        self.load_ingredients()

    def load_prep_methods(self) -> None:
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
        self.method_list = self.create_treeview(4, 1, 0, ('Id', 'Pasos'))
        self.load_prep_methods()

    def get_last_recipe_id(self) -> int:
        '''Obtiene el id del ultimo item de la lista de recetas y lo regresa, si no existe devuelve 0'''
        with open(RECIPE_LIST, newline="\n") as csvfile:
            last_id = 0
            reader = csv.DictReader(csvfile)
            for recipe in reader:
                if recipe['id'] != 'id' or recipe['id'] != '\n':
                    id = int(recipe['id'])
                    last_id = id
                else:
                    pass
            if last_id != 0:
                return last_id
            else:
                return 0

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
            cooking_time = self.cooking_time.get(),
            image = self.image,
            tags = self.tags.get(),
            favorite= self.favorite.get()
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

    def add_image(self) -> None:
        '''Guarda la direccion de la imagen a guardar'''
        self.image = fd.askopenfilename(
            filetypes=(
                ('jpg files', '*.jpg'), ('All files', '*.*')
            )
        )
        if self.image != None:
            msg.showinfo(
                message='Imagen agregada con exito',
                title='Agregar imagen',
                parent=self.parent 
            )
        else:
            msg.showinfo(
                message='Imagen no guardada', 
                title='Agregar imagen',
                parent=self.parent 
        )

    def delete_method(self) -> None:
        '''Borra el ultimo paso de preparacion de la lista'''
        try:
            method_list = []
            fields = ["id", "paso"]
            with open(METHOD_LIST,  "r", newline="\n") as csvfile:
                reader = csv.reader(csvfile)
                for prep_method in reader:
                    if prep_method[0] == "id":
                        pass
                    else:
                        method_list.append(prep_method)
            method_list.pop()
            with open(METHOD_LIST, "w", newline="\n") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                for prep_method in method_list:
                    writer.writerow(
                        {
                            'id': prep_method[0],
                            'paso': prep_method[1]
                        }
                    )
            self.refresh_method_tree()
        except IndexError:
            msg.showerror(message='No hay ningun paso en la lista', title='Eliminar paso de preparacion', parent = self.parent)

    def delete_ingredient(self) -> None:
        '''Borra el ultimo ingrediente de la lista'''
        try:
            ingredient_list = []
            fields = ["nombre", "cantidad", "medida"]
            with open(INGREDIENT_LIST,  "r", newline="\n") as csvfile:
                reader = csv.reader(csvfile)
                for ingredient in reader:
                    if ingredient[0] == "nombre":
                        pass
                    else:
                        ingredient_list.append(ingredient)
            ingredient_list.pop()
            with open(INGREDIENT_LIST, "w", newline="\n") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                for ingredient in ingredient_list:
                    writer.writerow(
                        {
                            'nombre': ingredient[0],
                            'cantidad': ingredient[1],
                            'medida': ingredient[2]
                        }
                    )
            self.refresh_ingredient_tree()
        except IndexError:
            msg.showerror(message='No hay ningun ingrediente en la lista',
                          title='Eliminar ingrediente',
                          parent = self.parent)

    def save(self) -> None:
        '''Toma los datos ingresados en la ventana y los almacena en csv_files'''
        new_recipe = self.get_recipe()
        fields = ['id', 'nombre', 'ingredientes', 'cantidades', 'preparacion', 'tiempo de preparacion', 'tiempo de coccion', 'creado', 'imagen', 'etiquetas', 'favorito']
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
                    'creado': new_recipe['creado'],
                    'imagen': new_recipe['imagen'],
                    'etiquetas': new_recipe['etiquetas'],
                    'favorito': new_recipe['favorito']
                }
            )
        self.parent.destroy()
        msg.showinfo(message='Receta creada, actualice la lista',
                      title='Receta agregada')
