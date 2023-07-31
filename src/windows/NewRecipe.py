from src.windows.AddIngredient import *
from src.windows.AddMethod import *
from constant import IMAGES_DIR 
from src.windows.IBaseWindow import *
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import shutil
from datetime import datetime

class NewRecipe(ttk.Frame, IBaseWindow):
    def __init__(self, parent, title: str, recipe_instance) -> None:
        ttk.Frame.__init__(self, parent, padding=(20))
        IBaseWindow.__init__(self, parent, title)
        
        self.recipe_instance = recipe_instance

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
        """Creates the user interface for creating a new recipe.

        This method sets up the user interface for creating a new recipe. It includes
        elements such as the "Imagen" label and the "Agregar" button to add an image,
        and it uses the `base_ui_config()` method to create the common elements like
        labels, entry fields, and buttons for managing ingredients and preparation steps.
        """
        # IMAGEN
        ttk.Label(self.parent, text="Imagen:", padding=3).grid(
            row=7, column=1, columnspan=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar", command=self.add_image).grid(
            row=7, column=2, columnspan=4, sticky=tk.EW)

        self.base_ui_config('Crear')

# INGREDIENTS ----------------------------------------

    def load_ingredients(self) -> None:
        """Reads the ingredients from the list of ingredients and displays them in the Treeview.

        This method is responsible for reading the list of ingredients (`tree_ing_data`)
        and displaying them in the `ingredient_list` Treeview. It iterates over each
        ingredient and inserts it into the Treeview for the user to view.
        """
        for ingredient in self.tree_ing_data:
            data = [ingredient[0], ingredient[1]]
            self.ingredient_list.insert('', tk.END, values=data)

    def new_ingredient(self) -> None: 
        """Opens a window to add a new ingredient.

        This method opens a new window (a `Toplevel` widget) to allow the user to add
        a new ingredient to the recipe. It creates an instance of the `AddIngredient` class
        and waits for the window to be closed. After the window is closed, it checks the
        `add_flag` attribute to see if a new ingredient was successfully added. If a new
        ingredient was added, it updates the `ingredients_temp` list and the `tree_ing_data`
        list with the new ingredient data and then refreshes the `ingredient_list` Treeview.
        """
        toplevel = tk.Toplevel(self.parent)
        add_ingredient_window = AddIngredient(toplevel, self).grid()
        toplevel.wait_window(add_ingredient_window)
        if self.add_flag:
            self.ingredients_temp.append(self.ingredient_value)
            self.tree_ing_data.append(self.data_ing)
            self.refresh_ingredient_tree()
            self.add_flag = False

    def refresh_ingredient_tree(self) -> None:
        """Refreshes the ingredient list in the Treeview.

        This method recreates the `ingredient_list` Treeview with updated data from the
        `tree_ing_data` list. It first calls the `create_treeview` method to create a new
        Treeview with the appropriate columns. Then, it calls the `load_ingredients` method
        to load the ingredient data from `tree_ing_data` into the newly created Treeview.
        """
        self.ingredient_list = self.create_treeview(2, 1, 1, ('Cantidad', 'Ingredientes'))
        self.load_ingredients()

    def delete_ingredient(self) -> None:
        """Deletes the last ingredient from the list.

        This method removes the last ingredient from the `ingredients_temp` list, which
        holds the IDs of ingredients associated with the recipe. It also removes the last
        ingredient from the `tree_ing_data` list, which holds the ingredient data to be
        displayed in the `ingredient_list` Treeview. After deleting the ingredient, it
        refreshes the `ingredient_list` Treeview to reflect the updated data.

        If there are no ingredients to delete (i.e., the `ingredients_temp` list is empty),
        it shows an error message to inform the user.
        """
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
        """Loads the preparation steps into the method list Treeview.

        This method reads the preparation steps from the `prep_desc_list` and displays them
        in the `method_list` Treeview. The `prep_desc_list` contains the descriptions of the
        preparation steps. It iterates through the `prep_desc_list`, and for each step,
        creates a new row in the Treeview with the order number and the preparation detail.
        The order number starts from 1 and increments for each preparation step.
        """
        for order, detail in enumerate(self.prep_desc_list, start=1):
            data = [order, detail]
            self.method_list.insert('', tk.END, values=data)

    def new_method(self) -> None:
        """Opens a window to add a new preparation step to the list.

        This method opens a new top-level window using the `AddMethod` class to allow the
        user to add a new preparation step. It waits for the user to close the window by
        using `wait_window`. If the user adds a new preparation step (`add_flag` is True),
        the method appends the new step's ID and description to `prep_id_list` and
        `prep_desc_list`, respectively. Then, it refreshes the `method_list` Treeview using
        the `refresh_method_tree` method to display the updated list of preparation steps.
        """
        toplevel = tk.Toplevel(self.parent)
        add_prep_method_window = AddMethod(toplevel, self).grid()
        toplevel.wait_window(add_prep_method_window)
        if self.add_flag:
            self.prep_id_list.append(self.prep_id)
            self.prep_desc_list.append(self.prep_desc)
            self.refresh_method_tree()
            self.add_flag = False

    def refresh_method_tree(self) -> None:
        """Refreshes the method list Treeview with the updated preparation steps.

        This method updates the `method_list` Treeview with the latest preparation steps
        by first clearing the current Treeview and then re-populating it. It calls the
        `create_treeview` method with appropriate parameters to create a new Treeview with
        two columns: 'Id' and 'Pasos'. Then, it calls the `load_prep_methods` method to
        load the preparation steps from `prep_desc_list` into the Treeview. This method is
        typically called after adding or deleting a preparation step to ensure the latest
        data is displayed.
        """
        self.method_list = self.create_treeview(4, 1, 0, ('Id', 'Pasos'))
        self.load_prep_methods()

    def delete_method(self) -> None:
        """Deletes the last preparation step from the list.

        This method removes the last preparation step from the `prep_id_list` and
        `prep_desc_list`. It then calls the `db_utils.delete_prep_method` method to delete
        the corresponding preparation step from the database. After that, it calls
        `refresh_method_tree` to update the `method_list` Treeview with the updated list of
        preparation steps. If there are no preparation steps left to delete, it displays an
        error message using the `msg.showerror` method.
        """
        try:
            self.db_utils.delete_prep_method(self.prep_id_list.pop())
            self.prep_desc_list.pop()
            self.refresh_method_tree()
        except IndexError:
            msg.showerror(message='No hay ningun paso en la lista', title='Eliminar paso de preparacion', parent = self.parent)

# ??? ----------------------------------------

    def add_image(self) -> None:
        """Opens a file dialog to select an image file and saves its path.

        This method opens a file dialog to allow the user to select an image file (JPG format).
        The selected image path is stored in the `image` attribute of the class. If the user
        cancels the file dialog, the `image` attribute remains `None`. After selecting an
        image, the method displays a message using `msg.showinfo` indicating whether the image
        was added successfully or not.
        """
        self.image = fd.askopenfilename(filetypes=(('jpg files', '*.jpg'), ('All files', '*.*')))
        if self.image != None:
            msg.showinfo(message='Imagen agregada con exito', title='Agregar imagen', parent=self.parent )
        else:
            msg.showinfo(message='Imagen no guardada',  title='Agregar imagen', parent=self.parent)

    def get_source(self, image: str) -> str:
        """Copies the selected image to the images folder and returns its relative path.

        This method takes the `image` path as input and copies the image file to the images
        folder (IMAGES_DIR). It returns the relative path of the copied image file (using
        backslashes as path separators for Windows systems). If the `image` is `None`, it
        returns `None` as there is no image to copy. If any error occurs during the image
        copying process, it displays an error message using `msg.showerror`.

        Parameters
        ---------
            image (str): The path of the selected image file.

        Returns
        -------
            str: The relative path of the copied image file, or None if `image` is None.
        """
        try:
            if image != None:
                shutil.copy(image, IMAGES_DIR)
                img_name = image.split('/')[-1]
                return "images\\" + img_name  # CORREGIR FORMATO
            else:
                return None
        except:
            msg.showerror(message='Un error sucedio durante la creacion de la imagen', title='Agregar Imagen')

    def get_fav(self, favorite: str) -> int:
        """Converts the favorite option to an integer value.

        Parameters
        ----------
            favorite (str): The favorite option, either 'Si' or 'No'.

        Returns
        -------
            int: The integer representation of the favorite option (1 or 0).
        """
        return 1 if favorite == 'Si' else 0

    def get_tag_list(self, tags: str) -> list[str]:
        """Extracts and returns a list of tags from a comma-separated string.

        This method takes a comma-separated `tags` string as input and extracts individual
        tags by splitting the string at each comma. It removes any leading and trailing spaces
        from each tag and returns a list containing all the extracted tags.

        Parameters
        ----------
            tags (str): A comma-separated string containing tags.

        Returns
        -------
            list[str]: A list of individual tags extracted from the input string.
        """
        tag_list = tags.replace(' ', '').split(',')
        return tag_list

    def get_tags_id(self, tags: str) -> list[int]:
        """Converts the comma-separated tags string to a list of tag IDs.

        This method takes the `tags` string as input, splits it using commas, and creates tags
        in the database for each individual tag if they do not exist. It then retrieves the
        IDs of the created tags and returns them as a list. If a tag already exists in the
        database, its ID will be retrieved instead of creating a new entry.

        Parameters
        ----------
            tags (str): The comma-separated tags string.

        Returns
        -------
            list[int]: A list of tag IDs for the given tags.
        """
        tag_list = self.get_tag_list(tags)
        tag_id_list = []
        for tag in tag_list:
            tag_id = self.db_utils.create_tag(tag)
            tag_id_list.append(tag_id)
        return tag_id_list

    def recipe_tags(self, tag_list: list[int], recipe_id: int) -> None:
        """Associates tags with a recipe in the database.

        This method takes a list of tag IDs (`tag_list`) and associates each tag with the
        recipe identified by the given `recipe_id`. It creates entries in the database linking
        the recipe with its corresponding tags.

        Parameters
        ----------
            tag_list (list[int]): A list of tag IDs to be associated with the recipe.
            recipe_id (int): The ID of the recipe to which the tags will be associated.
        """
        for tag in tag_list:
            self.db_utils.create_tag_recipe(tag, recipe_id)

    def recipe_ingredients(self, ingredients_ids: list[int], recipe_id: int):
        """Associates ingredients with a recipe in the database.

        This method takes a list of ingredient IDs (`ingredients_ids`) and associates each
        ingredient with the recipe identified by the given `recipe_id`. It creates entries in
        the database linking the recipe with its corresponding ingredients.

        Parameters
        ----------
            ingredients_ids (list[int]): A list of ingredient IDs to be associated with the recipe.
            recipe_id (int): The ID of the recipe to which the ingredients will be associated.
        """
        for id in ingredients_ids:
            self.db_utils.add_recipe_id_to_ingredients(id, recipe_id)

    def recipe_prep_methods(self, prep_method_ids: list[int], recipe_id: int) -> None:
        """Associates preparation methods with a recipe in the database.

        This method takes a list of preparation method IDs (`prep_method_ids`) and associates
        each preparation method with the recipe identified by the given `recipe_id`. It creates
        entries in the database linking the recipe with its corresponding preparation methods
        and stores the order of the methods for the recipe.

        Parameters
        ----------
            prep_method_ids (list[int]): A list of preparation method IDs to be associated with the recipe.
            recipe_id (int): The ID of the recipe to which the preparation methods will be associated.
        """
        for order, method_id in enumerate(prep_method_ids, start=1):
            self.db_utils.add_prep_method_to_recipe(method_id, order, recipe_id)

    def save(self) -> None:
        """Stores the entered recipe data into the database.

        This method retrieves the data entered by the user in the window and stores it into the
        database as a new recipe. It uses various helper methods to create tags, associate tags,
        ingredients, and preparation methods with the new recipe, and then closes the window.
        """
        try:
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

            self.close_window(
                {
                    'id': recipe_id,
                    'name': new_recipe['name'],
                    'ingredients': self.tree_ing_data,
                    'prep_time': new_recipe['prep_time'],
                    'cook_time': new_recipe['cook_time'],
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            )
        except Exception as e:
            msg.showerror(message=f'Error: {e}', title='Nueva Receta', parent = self.parent)

    def close_window(self, new_data: dict) -> None:
        """Closes the window after adding a new recipe.

        This method takes `new_data` as input, which is a dictionary containing the details of
        the newly added recipe. It sets the `added_row` attribute of the `recipe_instance`
        and sets the `new_flag` attribute to indicate that a new recipe was added. Then, it
        closes the window.

        Parameters
        ----------
            new_data (dict): A dictionary containing the details of the newly added recipe.
        """
        self.recipe_instance.added_row = new_data
        self.recipe_instance.new_flag = True
        self.parent.destroy()

    def __del__(self):
        """Disconnects from the database when the object is deleted.

        This method is called when the object is deleted or goes out of scope. It ensures that
        the connection to the database is closed to avoid resource leaks.
        """
        self.db_utils.disconnect()
