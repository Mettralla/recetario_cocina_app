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
    """
    Class representing the window to edit a recipe.

    This class allows the user to edit an existing recipe. It inherits from `ttk.Frame` and `IBaseWindow`, providing
    common configurations for the window.

    Parameters
    ----------
        parent (tk.Tk or tk.Toplevel): The parent window to which this window is associated.
        title (str): The title of the window.
        recipe_id (int): The ID of the recipe to be edited.
        recipe_instance: An instance of the recipe to be edited.
    """
    def __init__(self, parent, title: str, recipe_id: int, recipe_instance) -> None:
        ttk.Frame.__init__(self, parent, padding=(20))
        IBaseWindow.__init__(self, parent, title)

        self.db_utils = DBUtils()
        self.db_utils.connect()

        self.id = recipe_id
        self.recipe_instance = recipe_instance
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
        """Creates the user interface for editing the recipe.

        This method sets up the user interface elements for editing an existing recipe.
        It adds a label for the "Imagen" section and buttons for adding and deleting an image.
        It also calls the base_ui_config method to set up the common UI elements for the recipe.
        """
        # IMAGEN
        ttk.Label(self.parent, text="Imagen:", padding=3).grid(
            row=7, column=1, columnspan=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar", command=self.add_image).grid(
            row=7, column=2, columnspan=3, sticky=tk.EW)
        ttk.Button(self.parent, text="Borrar", command=self.delete_image).grid(
            row=7, column=5, sticky=tk.EW)
        
        self.base_ui_config('Guardar Cambios')

    def set_variables(self):
        """Sets the values of the entry fields with the current recipe data.

        This method populates the entry fields with the values from the existing recipe data
        to display them for editing. It sets the "nombre," "tiempo de preparacion," "tiempo de coccion," 
        "etiquetas," and "favorito" fields to their respective values from the database.
        """
        self.name.set(self.recipe['nombre'])
        self.preparation_time.set(self.recipe['tiempo de preparacion'])
        self.cooking_time.set(self.recipe['tiempo de coccion'])
        self.tags.set(self.recipe['etiquetas'])
        self.favorite.set('Si' if self.recipe['favorito'] == 1 else 'No')

    def load_ingredients(self) -> None:
        """Loads the ingredients into the Treeview.

        This method retrieves the ingredient and quantity data from the recipe and inserts
        them into the ingredient_list Treeview. Each ingredient is displayed as a row with its corresponding
        quantity in the Treeview.
        """
        ingredients = self.recipe['ingredientes'].split(',')
        amounts = self.recipe['cantidades'].split(',')
        for i  in range(len(ingredients)):
            if len(ingredients) != 0:
                self.ingredient_list.insert(
                '', tk.END, values=[amounts[i], ingredients[i]])

    def new_ingredient(self) -> None:
        """Opens a new window to add a new ingredient.

        This method opens a new window (top-level) to allow the user to add a new ingredient
        to the recipe. The AddIngredient class is used to manage the new ingredient input.
        After the ingredient is added, the method updates the recipe data and refreshes the
        ingredient_list Treeview.
        """
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
        """Refreshes the list of ingredients in the Treeview.

        This method updates the `ingredient_list` Treeview with the current ingredient data
        in the `recipe` dictionary. It creates a new Treeview widget and loads the updated
        ingredients from the recipe. If no changes were made, it displays an error message.
        """
        try:
            self.ingredient_list = self.create_treeview(2, 1, 1, ('Cantidad', 'Ingredientes'))
            self.load_ingredients()
        except UnboundLocalError:
            msg.showerror(message='No realizo ningun cambio', title='Error al actualizar', parent = self.parent)

    def delete_ingredient(self) -> None:
        """Deletes the last ingredient from the list of ingredients.

        This method removes the last ingredient from the `ingredient_list` Treeview and
        the corresponding data from the `recipe` dictionary. It also updates the
        `ingredients_temp` and `tree_ing_data` lists. If there are no ingredients left to delete,
        it displays an error message.
        """
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
        """Loads the preparation steps into the Treeview.

        This method retrieves the preparation steps from the `recipe` dictionary, splits
        them into separate steps, and inserts them into the `method_list` Treeview.
        The steps are enumerated starting from 1.
        """
        prep_methods = self.recipe['preparacion'].split(',')
        for i, prep_method in enumerate(prep_methods, start=1):
            if len(prep_method) != 0:
                self.method_list.insert('', tk.END, values=[i, prep_method])

    def new_method(self) -> None:
        """Opens a window to add a new preparation step.

        This method opens a new window where the user can input a new preparation step.
        The step is added to the `method_list` Treeview and the `recipe` dictionary.
        It also updates the `prep_id_list` and `prep_desc_list` with the new step's data.
        If the user cancels without adding a step, no changes are made.
        """
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
        """Updates the preparation steps list.

        This method refreshes the `method_list` Treeview by recreating it and
        loading the preparation steps from the `recipe` dictionary.
        """
        try:
            self.method_list = self.create_treeview(4, 1, 0, ('Id', 'Pasos'))
            self.load_prep_methods()
        except UnboundLocalError:
            msg.showerror(message='No realizo ningun cambio',
                          title='Error al actualizar', parent=self.parent)

    def delete_method(self) -> None:
        """Deletes the last preparation step from the list.

        This method removes the last preparation step from the `method_list` Treeview
        and the `recipe` dictionary. It also updates the `prep_id_list` and `prep_desc_list`.
        If there are no steps to delete, it shows an error message.
        """
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
        """Saves the image file path to be stored.

        This method opens a file dialog where the user can choose an image file to be
        associated with the recipe. The chosen image is copied to the IMAGES_DIR folder
        and the file path is saved in the `recipe` dictionary. If no image is selected,
        a message is shown indicating that the image was not saved.
        """
        self.image = fd.askopenfilename(filetypes=(('jpg files', '*.jpg'), ('All files', '*.*')))
        if self.image != None:
            shutil.copy(self.image, IMAGES_DIR)
            img_name = self.image.split('/')[-1]
            self.recipe['imagen'] = "images\\" + img_name  # CORREGIR FORMATO
            msg.showinfo(message='Imagen agregada con exito', title='Agregar imagen',parent=self.parent)
        else:
            msg.showinfo(message='Imagen no guardada', title='Agregar imagen', parent=self.parent)

    def delete_image(self) -> None:
        """Deletes the associated image of the recipe.

        This method checks if the recipe has an associated image. If there is no image,
        it shows an information message. If an image is found, it deletes the file
        and updates the `recipe` dictionary to remove the image reference. A success
        message is displayed after deleting the image.
        """
        if self.recipe['imagen'] == None:
            msg.showinfo(title='Borrar imagen', message='Esta receta no tiene imagen', parent=self.parent)
        else:
            os.remove(self.recipe['imagen'])
            self.recipe['imagen'] = None
            msg.showinfo(title='Borrar imagen', message='Imagen borrada', parent = self.parent)

    def save(self) -> None:
        """Saves the edited recipe to the database.

        This method retrieves the edited data from the entry fields, updates the recipe's
        name, preparation time, cooking time, and favorite status in the `recipe` dictionary.
        Then, it creates a dictionary with the edited recipe data, including ingredient IDs
        and preparation method IDs. The `db_utils.update_recipe()` method is called to update
        the recipe in the database, and `db_utils.check_and_update()` is used to update
        the ingredients and preparation methods. Finally, the `close_window()` method is called
        to close the current window and pass the edited recipe data back to the parent window.
        """
        try:
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
            self.close_window([
                updated_values['nombre'],
                edited_recipe['ingredientes'],
                updated_values['tiempo de preparacion'],
                updated_values['tiempo de coccion'],
            ])
        except Exception as e:
            msg.showerror(message=f'Error: {e}', title='Editar Receta', parent = self.parent)
        
    def close_window(self, edit_data: list) -> None:
        """Closes the current window and passes the edited data to the parent window.

        This method sets the `edited_row` and `edit_flag` attributes of the `recipe_instance`
        to pass the edited data back to the parent window. It then destroys the current window.

        Args:
            edit_data (list): A list containing the edited recipe data to be passed back.
        """
        self.recipe_instance.edited_row = edit_data
        self.recipe_instance.edit_flag = True
        self.parent.destroy()
    
    def __del__(self):
        """Destructor method to disconnect from the database.

        This method is automatically called when the instance of the class is deleted. It disconnects from the database
        to release the resources.
        """
        self.db_utils.disconnect()
