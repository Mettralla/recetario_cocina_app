import tkinter as tk
from tkinter import ttk
from src.utils.db_utils import DBUtils
from tkinter import messagebox as msg

class AddIngredient(ttk.Frame):
    """Class representing the window for adding individual ingredients.

    This class creates a window to add a new ingredient to the current recipe.
    It provides a user interface to enter the name, quantity, and measurement of the ingredient.
    Upon adding the ingredient, it connects to the database via the 'db_utils' object,
    and associates the ingredient with the current recipe using the 'add_ingredient_to_recipe' method.
    The class also handles window closure and updates the parent recipe instance with the data of the new ingredient.

    Attributes
    ----------
        parent (Tk): The main window where the add ingredient window will be displayed.
        recipe_instance (Recipe): The instance of the current recipe being edited.

    Methods
    -------
        __init__(self, parent, recipe_instance): Constructor of the class.
        add_ingredient(self): Adds a new ingredient to the current recipe.
        close_window(self, ingredient_value, new_ingredient): Closes the window and updates the parent recipe instance.
        __del__(self): Destructor of the class that disconnects from the 'db_utils' object.

    Attributes
    ----------
        self.parent (Tk): The main window where the add ingredient window will be displayed.
        self.recipe_instance (Recipe): The instance of the current recipe being edited.
        self.db_utils (DBUtils): An object handling the connection and queries to the database.
        self.ingrediente (tk.StringVar): Control variable for the name of the ingredient.
        self.cantidad (tk.IntVar): Control variable for the quantity of the ingredient.
        self.medida (tk.StringVar): Control variable for the measurement of the ingredient.
        self.medidas (list): List of measurement options for the ingredient.
    """
    def __init__(self, parent, recipe_instance) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.recipe_instance = recipe_instance

        self.db_utils = DBUtils()
        self.db_utils.connect()

        parent.title('Ingredientes')
        parent.geometry('250x140')
        parent.resizable(0, 0)
        parent.config(bg='#d9d9d9')

        # NOMBRE DEL INGREDIENTE
        self.ingrediente = tk.StringVar()
        # CANTIDAD DEL INGREDIENTE
        self.cantidad = tk.IntVar()
        # MEDIDA QUE SE USA PARA CUANTIFICAR LA CANTIDAD  
        self.medida = tk.StringVar()
        # OPCIONES DE MEDIDA
        self.medidas = ['miligramos', 'gramos', 'kilogramos',
                        'cucharadas', 'cucharaditas', 'unidades', 'taza', 'mililitros', 'litros', 'a gusto']

        # GRID
        # COLUMNS
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=1)

        # ROWS
        parent.rowconfigure(0, weight=1)  
        parent.rowconfigure(1, weight=2)  
        parent.rowconfigure(2, weight=2)  
        parent.rowconfigure(3, weight=1)  

        # AGREGAR INGREDIENTES UI
        # NOMBRE DEL INGREDIENTE
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(
            row=0, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.ingrediente, justify=tk.RIGHT).grid(
            row=0, column=2, sticky=tk.EW)
        # CANTIDAD DEL INGREDIENTE
        ttk.Label(self.parent, text="Cantidad:", padding=3).grid(
            row=1, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.cantidad, justify=tk.RIGHT).grid(
            row=1, column=2, sticky=tk.EW, padx=5)
        # SELECCIONAR MEDIDA
        ttk.Label(self.parent, text="Medida:", padding=3).grid(
            row=2, column=1, sticky=tk.EW)
        ttk.Combobox(self.parent, textvariable=self.medida, values=self.medidas, justify=tk.RIGHT).grid(
            row=2, column=2, sticky=tk.EW)
        # BOTONES : AGREGAR || CANCELAR
        ttk.Button(self.parent, text="Agregar", command=self.add_ingredient).grid(
            row=3, column=0, padx=5, columnspan=2, sticky=tk.EW)
        ttk.Button(self.parent, text="Cancelar", command=self.parent.destroy).grid(
            row=3, column=2, padx=5, columnspan=2, sticky=tk.EW)

    def add_ingredient(self):
        """Add a new ingredient to the recipe.

        This method takes the input values for a new ingredient (name, quantity, and unit of measurement),
        creates the ingredient in the database using the 'create_ingredient' method from 'db_utils',
        and then associates the ingredient with the current recipe using the 'add_ingredient_to_recipe' method.
        Finally, it closes the current window and updates the parent recipe instance with the new ingredient data.

        If an error occurs during the process, an error message will be displayed in a pop-up window.

        Raises:
            Exception: If any error occurs during the ingredient creation or association process.
        """
        try:
            new_ingredient = {
                "nombre": self.ingrediente.get(),
                "cantidad": self.cantidad.get(),
                "medida": self.medida.get()
            }
            new_ingredient_id = self.db_utils.create_ingredient(new_ingredient['nombre'])
            ingredient_value = self.db_utils.add_ingredient_to_recipe(new_ingredient_id, new_ingredient['cantidad'], new_ingredient['medida'])
            self.close_window(ingredient_value, new_ingredient)
        except Exception as e:
            msg.showerror(message=f'Error: {e}', title='Nuevo Ingrediente', parent = self.parent)

    def close_window(self, ingredient_value: int, new_ingredient: dict) -> None:
        """Close the ingredient window and update the parent recipe instance.

        This method is called after successfully adding an ingredient to the recipe.
        It updates the parent recipe instance with the ingredient's database ID (ingredient_value),
        the formatted ingredient data (data_ing), and sets the 'add_flag' to True to indicate a new ingredient was added.
        Finally, it closes the current window.

        Parameters:
            ingredient_value (int): The ID of the newly created ingredient in the database.
            new_ingredient (dict): A dictionary containing the details of the new ingredient.

        Note:
            The 'recipe_instance' and 'parent' attributes are assumed to be available in the current instance.
        """
        self.recipe_instance.ingredient_value = ingredient_value
        self.recipe_instance.data_ing = (str(new_ingredient['cantidad']) + ' ' + new_ingredient['medida'], new_ingredient['nombre'])
        self.recipe_instance.add_flag = True
        self.parent.destroy()

    def __del__(self) -> None:
        """Disconnect from the database when the instance is deleted.

        This method is called automatically when the instance is being deleted or garbage-collected.
        It ensures that the 'db_utils' object disconnects from the database to free up resources.
        """
        self.db_utils.disconnect()
