from src.windows.AddIngredient import *
from src.windows.AddMethod import *
from constant import IMAGES_DIR 
from src.windows.IBaseWindow import *
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import shutil

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

        # GUARDA LOS IDS DE INGREDIENTES_RECETA
        self.ingredient_value = None
        self.ingredients_temp = []
        
        self.add_flag = False

        #RECIBE LOS DATOS DEL TOP LEVEL
        self.data_ing = None
        # GUARDA NOMBRE Y MEDIDAS
        self.tree_ing_data = []
        
        # RECIBE LOS DATOS DE TOP LEVEL
        # IDS
        self.prep_id = None
        self.prep_id_list = []
        # DESCRICIONES
        self.prep_desc = None
        self.prep_desc_list = []

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

# INGREDIENTS ----------------------------------------

    def load_ingredients(self) -> None:
        '''Lee el los ingredientes de la lista de ingredientes y los muestra'''
        for ingredient in self.tree_ing_data:
            data = [ingredient[0], ingredient[1]]
            self.ingredient_list.insert('', tk.END, values=data)

    def new_ingredient(self) -> None: 
        '''Abre una ventana para agregar un ingrediente'''
        toplevel = tk.Toplevel(self.parent)
        add_ingredient_window = AddIngredient(toplevel, self).grid()
        toplevel.wait_window(add_ingredient_window)
        if self.add_flag:
            self.ingredients_temp.append(self.ingredient_value)
            self.tree_ing_data.append(self.data_ing)
            self.refresh_ingredient_tree()
            self.add_flag = False

    def refresh_ingredient_tree(self) -> None:
        '''Actualiza la lista de ingredientes'''
        self.ingredient_list = self.create_treeview(2, 1, 1, ('Cantidad', 'Ingredientes'))
        self.load_ingredients()

    def delete_ingredient(self) -> None:
        '''Borra el ultimo ingrediente de la lista'''
        try:
            self.db_utils.delete_ingredient_to_recipe(self.ingredients_temp.pop())
            self.tree_ing_data.pop()
            self.refresh_ingredient_tree()
        except IndexError:
            msg.showerror(message='No hay ningun ingrediente en la lista',
                          title='Eliminar ingrediente',
                          parent = self.parent)

# PREP METHODS ----------------------------------------

    def load_prep_methods(self) -> None:
        '''Lee los pasos de preparacion de la lista de pasos y los muestra'''
        for order, detail in enumerate(self.prep_desc_list, start=1):
            data = [order, detail]
            self.method_list.insert('', tk.END, values=data)

    def new_method(self) -> None:
        '''Crea una ventana para agregar un paso a la lista de preparacion'''
        toplevel = tk.Toplevel(self.parent)
        add_prep_method_window = AddMethod(toplevel, self).grid()
        toplevel.wait_window(add_prep_method_window)
        if self.add_flag:
            self.prep_id_list.append(self.prep_id)
            self.prep_desc_list.append(self.prep_desc)
            self.refresh_method_tree()
            self.add_flag = False

    def refresh_method_tree(self) -> None:
        '''Actualiza la lista de pasos de preparacion'''
        self.method_list = self.create_treeview(4, 1, 0, ('Id', 'Pasos'))
        self.load_prep_methods()

    def delete_method(self) -> None:
        '''Borra el ultimo paso de preparacion de la lista'''
        try:
            self.db_utils.delete_prep_method(self.prep_id_list.pop())
            self.prep_desc_list.pop()
            self.refresh_method_tree()
        except IndexError:
            msg.showerror(message='No hay ningun paso en la lista', title='Eliminar paso de preparacion', parent = self.parent)

# ??? ----------------------------------------

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

    def get_source(self, image: str) -> str:
        '''Copia la imagen a la carpeta de imagenes y devuelve el ruta'''
        try:
            if image != None:
                shutil.copy(image, IMAGES_DIR)
                img_name = image.split('/')[-1]
                return "images\\" + img_name  # CORREGIR FORMATO
            else:
                return None
        except:
            msg.showerror(
                message='Un error sucedio durante la creacion de la imagen', title='Agregar Imagen')

    def get_fav(self, favorite):
        return 1 if favorite == 'Si' else 0

    def get_tag_list(self, tags):
        tag_list = tags.replace(' ', '').split(',')
        return tag_list

    def get_tags_id(self, tags: str) -> list[int]:
        tag_list = self.get_tag_list(tags)
        tag_id_list = []
        for tag in tag_list:
            tag_id = self.db_utils.create_tag(tag)
            tag_id_list.append(tag_id)
        return tag_id_list

    def recipe_tags(self, tag_list, recipe_id):
        for tag in tag_list:
            self.db_utils.create_tag_recipe(tag, recipe_id)

    def recipe_ingredients(self, ingredients_ids, recipe_id):
        for id in ingredients_ids:
            self.db_utils.add_recipe_id_to_ingredients(id, recipe_id)

    def recipe_prep_methods(self, prep_method_ids, recipe_id):
        for order, method_id in enumerate(prep_method_ids, start=1):
            self.db_utils.add_prep_method_to_recipe(method_id, order, recipe_id)

    def save(self) -> None:
        '''Toma los datos ingresados en la ventana y los almacena en csv_files'''
        new_recipe = {
            'name': self.name.get(),
            'prep_time': self.preparation_time.get(),
            'cook_time': self.cooking_time.get(),
            'image': self.get_source(self.image),
            'favorite': self.get_fav(self.favorite.get()),
        }
        recipe_id = self.db_utils.create_recipe(new_recipe)
        tag_ids = self.get_tags_id(self.tags.get())
        self.recipe_tags(tag_ids, recipe_id)
        self.recipe_ingredients(self.ingredients_temp, recipe_id)
        self.recipe_prep_methods(self.prep_id_list, recipe_id)

        self.parent.destroy()
        msg.showinfo(message='Receta creada, actualice la lista',
        title='Receta agregada')

    def __del__(self):
        self.db_utils.disconnect()
