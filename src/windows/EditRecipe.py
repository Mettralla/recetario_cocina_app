from src.windows.AddIngredient import *
from src.windows.AddMethod import *
from src.windows.IBaseWindow import *
from constant import IMAGES_DIR 
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import itertools
import shutil
import os

class EditRecipe(ttk.Frame, IBaseWindow):
    def __init__(self, parent, title: str, recipe_id: int) -> None:
        ttk.Frame.__init__(self, parent, padding=(20))
        IBaseWindow.__init__(self, parent, title)

        self.db_utils = DBUtils()
        self.db_utils.connect()

        self.id = recipe_id
        self.recipe = self.db_utils.get_recipe_by_id(recipe_id)
        self.recipe_original = self.recipe.copy()
        self.add_flag = False

        self.name = tk.StringVar()
        self.preparation_time = tk.StringVar()
        self.cooking_time = tk.StringVar()
        self.tags = tk.StringVar()
        self.favorite = tk.StringVar()
        
        # GUARDA LOS IDS DE INGREDIENTES_RECETA
        self.ingredient_value = None
        self.ingredients_temp = []

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

        parent.rowconfigure(8, weight=1)  # buttons

        self.create_ui()
        self.set_variables()

    def create_ui(self) -> None:
        '''Crea la interfaz que usara el usuario para crear la receta'''
        # IMAGEN
        ttk.Label(self.parent, text="Imagen:", padding=3).grid(
            row=7, column=1, columnspan=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar", command=self.add_image).grid(
            row=7, column=2, columnspan=3, sticky=tk.EW)
        ttk.Button(self.parent, text="Borrar", command=self.delete_image).grid(
            row=7, column=5, sticky=tk.EW)
        
        self.base_ui_config('Guardar Cambios')

    def set_variables(self):
        '''Rellena automaticamente los entry con los valores actuales'''
        self.name.set(self.recipe['nombre'])
        self.preparation_time.set(self.recipe['tiempo de preparacion'])
        self.cooking_time.set(self.recipe['tiempo de coccion'])
        self.tags.set(self.recipe['etiquetas'])
        self.favorite.set('Si' if self.recipe['favorito'] == 1 else 'No')

    def load_ingredients(self) -> None:
        '''Carga los ingredientes de la lista en el Treeview'''
        ingredients = self.recipe['ingredientes'].split(',')
        amounts = self.recipe['cantidades'].split(',')
        for i  in range(len(ingredients)):
            if len(ingredients) != 0:
                self.ingredient_list.insert(
                '', tk.END, values=[amounts[i], ingredients[i]])

    def new_ingredient(self) -> None:
        '''Abre una ventana para agregar un ingrediente'''
        toplevel = tk.Toplevel(self.parent)
        add_ingredient_window = AddIngredient(toplevel, self).grid()
        toplevel.wait_window(add_ingredient_window)
        if self.add_flag:
            self.recipe['cantidades'] = f"{self.recipe['cantidades']},{self.data_ing[0]}"
            self.recipe['ingredientes'] = f"{self.recipe['ingredientes']},{self.data_ing[1]}"
            self.ingredients_temp.append(self.ingredient_value)
            self.tree_ing_data.append(self.data_ing[1])
            self.refresh_ingredient_tree()
            self.add_flag = False

    def refresh_ingredient_tree(self) -> None:
        '''Actualiza la lista de ingredientes'''
        try:
            self.ingredient_list = self.create_treeview(2, 1, 1, ('Cantidad', 'Ingredientes'))
            self.load_ingredients()
        except UnboundLocalError:
            msg.showerror(message='No realizo ningun cambio', title='Error al actualizar', parent = self.parent)

    def delete_ingredient(self) -> None:
        '''Elimina el ultimo ingrediente de la lista de ingredientes'''
        try:
            if self.ingredients_temp != []:
                self.db_utils.delete_ingredient_to_recipe(self.ingredients_temp.pop())
                self.tree_ing_data.pop()
            ingredients = self.recipe['ingredientes'].split(',')[:-1]
            amounts = self.recipe['cantidades'].split(',')[:-1]
            self.recipe['ingredientes'] = ','.join(ingredients)
            self.recipe['cantidades'] = ','.join(amounts)
            self.refresh_ingredient_tree()
        except IndexError:
            msg.showerror(message='No hay ningun ingrediente en la lista',
                          title='Eliminar ingrediente',
                          parent = self.parent)

# PREP METHOD ----------------------------------------------

    def load_prep_methods(self) -> None:
        '''Carga los ingredientes de la lista en el Treeview'''
        prep_methods = self.recipe['preparacion'].split(',')
        for i, prep_method in enumerate(prep_methods, start=1):
            if len(prep_method) != 0:
                self.method_list.insert('', tk.END, values=[i, prep_method])

    def new_method(self) -> None:
        '''Abre una ventana para agregar paso de preparacion'''
        toplevel = tk.Toplevel(self.parent)
        add_prep_method_window = AddMethod(toplevel, self).grid()
        toplevel.wait_window(add_prep_method_window)
        if self.add_flag:
            self.recipe['preparacion'] = f"{self.recipe['preparacion']},{self.prep_desc}"
            self.prep_id_list.append(self.prep_id)
            self.prep_desc_list.append(self.prep_desc)
            self.refresh_method_tree()
            self.add_flag = False

    def refresh_method_tree(self) -> None:
        '''Actualiza la lista de preparacion'''
        try:
            self.method_list = self.create_treeview(4, 1, 0, ('Id', 'Pasos'))
            self.load_prep_methods()
        except UnboundLocalError:
            msg.showerror(message='No realizo ningun cambio',
                          title='Error al actualizar', parent=self.parent)

    def delete_method(self) -> None:
        '''Elimina el ultimo elemento de la lista de preparacion'''
        try:
            if self.prep_id_list != []:
                self.db_utils.delete_prep_method(self.prep_id_list.pop())
                self.prep_desc_list.pop()
            prep = self.recipe['preparacion'].split(',')[:-1]
            self.recipe['preparacion'] = ','.join(prep)
            self.refresh_method_tree()
        except IndexError:
            msg.showerror(message='No hay ningun paso en la lista',
                          title='Eliminar ingrediente', parent=self.parent)

    def add_image(self) -> None:
        '''Guarda la direccion de la imagen a guardar'''
        self.image = fd.askopenfilename(
            filetypes=(
                ('jpg files', '*.jpg'), ('All files', '*.*')
            )
        )
        if self.image != None:
            shutil.copy(self.image, IMAGES_DIR)
            img_name = self.image.split('/')[-1]
            self.recipe['imagen'] = "images\\" + img_name  # CORREGIR FORMATO
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

    def delete_image(self) -> None:
        '''Elimina la receta si la encuentra'''
        if self.recipe['imagen'] == None:
            msg.showinfo(title='Borrar imagen', message='Esta receta no tiene imagen', parent=self.parent)
        else:
            os.remove(self.recipe['imagen'])
            self.recipe['imagen'] = None
            msg.showinfo(title='Borrar imagen', message='Imagen borrada', parent = self.parent)

    def save(self) -> None:
        '''Toma los datos ingresados en la ventana y los almacena en csv_files'''
        updated_values = {
            'id': self.id,
            'nombre': self.name.get(),
            'tiempo de preparacion': self.preparation_time.get(),
            'tiempo de coccion': self.cooking_time.get(),
            'imagen': self.recipe['imagen'],
            'favorito': 1 if self.favorite.get() == 'Si' else 0
        }
        self.db_utils.update_recipe(updated_values)
        edited_recipe = {
            'ingredientes': self.recipe['ingredientes'],
            'cantidades': self.recipe['cantidades'],
            'preparacion': self.recipe['preparacion'],
            'etiquetas': self.tags.get(),
            'ingredients_id': self.ingredients_temp,
            'methods_id': self.prep_id_list
        }
        self.db_utils.check_and_update(edited_recipe, self.recipe_original)
        self.parent.destroy()
