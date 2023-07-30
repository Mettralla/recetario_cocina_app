import tkinter as tk
from tkinter import ttk
from src.windows.IBaseWindow import *
from PIL import ImageTk, Image

class ReadRecipe(ttk.Frame, IBaseWindow):
    """Class representing the window to read a recipe.

    This class displays the details of a specific recipe on the window. It inherits from `ttk.Frame` and `IBaseWindow`,
    providing common configurations for the window.

    Parameters
    ----------
        parent (tk.Tk or tk.Toplevel): The parent window to which this window is associated.
        title (str): The title of the window.
        recipe_id (str): The ID of the recipe to be displayed.

    Attributes
    ----------
        db_utils (DBUtils): An instance of the DBUtils class for database-related operations.
        id (str): The ID of the recipe being displayed.
        recipe (dict): A dictionary containing the details of the recipe fetched from the database.
        star (ImageTk.PhotoImage): An ImageTk.PhotoImage object representing a filled star icon.
        empty_star (ImageTk.PhotoImage): An ImageTk.PhotoImage object representing an empty star icon.
        img (ImageTk.PhotoImage): An ImageTk.PhotoImage object representing the recipe's image.
        ingredient_list (ttk.Treeview): A Treeview widget to display the list of ingredients for the recipe.
        method_list (ttk.Treeview): A Treeview widget to display the list of preparation steps for the recipe.
    """
    def __init__(self, parent, title: str, recipe_id: str) -> None:
        ttk.Frame.__init__(self, parent, padding=(20))
        IBaseWindow.__init__(self, parent, title)

        self.db_utils = DBUtils()
        self.db_utils.connect()

        self.id = recipe_id
        self.recipe = self.db_utils.get_recipe_by_id(recipe_id)
        self.star = ImageTk.PhotoImage(
            Image.open('images\star.png').resize((30, 30)))
        self.empty_star = ImageTk.PhotoImage(
            Image.open('images\empty_star.png').resize((30, 30)))

        self.create_ui()

    def create_ui(self) -> None:
        """Create the user interface for displaying the recipe details.

        This method creates and arranges the widgets to display the recipe details, including the recipe name, image,
        ingredient list, preparation steps, preparation and cooking times, tags, and a "Close" button.
        """
        # TITULO
        if self.recipe['favorito'] == 1:
            ttk.Label(self.parent, text=self.recipe['nombre'], font=(
                'Arial', 25), image=self.star, compound=tk.LEFT, justify=tk.LEFT).grid(row=0, column=1)
        else: 
            ttk.Label(self.parent, text=self.recipe['nombre'], font=(
                'Arial', 25), image=self.empty_star, compound=tk.LEFT, justify=tk.LEFT).grid(row=0, column=1)
        
        # IMAGEN
        if self.recipe['imagen'] != None:
            self.img = ImageTk.PhotoImage(
                Image.open(self.recipe['imagen']).resize((100, 100)))
            ttk.Label(self.parent, image=self.img).grid(
                row=0, column=5)
        
        # LISTA DE INGREDIENTES
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(
            row=1, column=1, sticky=tk.EW)
        self.ingredient_list = self.create_treeview(2, 1, 1, ('Cantidad', 'Ingredientes'))
        self.load_ingredients()
        
        # LISTA DE PASOS DE PREPARACION
        ttk.Label(self.parent, text="Preparacion:", padding=3).grid(
            row=3, column=1, sticky=tk.EW)
        self.method_list = self.create_treeview(4, 1, 0, ('Id', 'Pasos'))
        self.load_method_list()
        
        # TIEMPO DE PREPARACION
        ttk.Label(self.parent, text=f"Tiempo de Preparacion: {self.recipe['tiempo de preparacion']} min", padding=3).grid(
            row=5, column=1, columnspan=3, sticky=tk.EW)
        
        # TIEMPO DE COCCION
        ttk.Label(self.parent, text=f"Tiempo de Cocción: {self.recipe['tiempo de coccion']} min", padding=3).grid(
            row=5, column=3, columnspan=3, sticky=tk.EW)
        
        ttk.Label(self.parent, text=f"Etiquetas: {self.recipe['etiquetas']}", padding=3).grid(
            row=6, column=1, columnspan=5, sticky=tk.EW)
        
        # BOTON
        ttk.Button(self.parent, text="Cerrar", command=self.parent.destroy).grid(
            row=7, column=1, columnspan=5, sticky=tk.NSEW, padx=5, pady=5)

    def load_ingredients(self) -> None:
        """Load the ingredients of the recipe into the ingredient_list Treeview.

        This method extracts the ingredients and their corresponding quantities from the recipe dictionary and inserts
        them into the ingredient_list Treeview for display.
        """
        ingredients = self.recipe['ingredientes'].split(',')
        amounts = self.recipe['cantidades'].split(',')
        for i in range(len(ingredients)):
            self.ingredient_list.insert(
                '', tk.END, values=[amounts[i], ingredients[i]])

    def load_method_list(self) -> None:
        """Load the preparation steps of the recipe into the method_list Treeview.

        This method extracts the preparation steps from the recipe dictionary and inserts them into the method_list
        Treeview for display.
        """
        prep_methods = self.recipe['preparacion'].split(',')
        # print(prep_methods)
        for index, prep_method in enumerate(prep_methods, 1):
            prep_value = prep_method.strip()
            self.method_list.insert(
                '', tk.END, values=[index, prep_value]
            )

    def __del__(self):
        """Destructor method to disconnect from the database.

        This method is automatically called when the instance of the class is deleted. It disconnects from the database
        to release the resources.
        """
        self.db_utils.disconnect()