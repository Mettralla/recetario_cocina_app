import tkinter as tk
from tkinter import ttk
from src.utils.db_utils import DBUtils
from tkinter import messagebox as msg

class AddMethod(ttk.Frame):
    """Class representing the window to add a new cooking method.

    This class creates a window to add a new cooking method to the current recipe.
    It provides a user interface to enter the name of the cooking method.
    Upon adding the cooking method, it connects to the database via the 'db_utils' object,
    and stores the new cooking method using the 'create_prep_method' method.
    The class also handles window closure and updates the parent recipe instance with the new cooking method data.

    Attributes
    ----------
        parent (Tk): The main window where the add method window will be displayed.
        recipe_instance (Recipe): The instance of the current recipe being edited.

    Methods
    -------
        add_method(self): Adds a new cooking method to the current recipe.
        close_window(self, new_prep_method, prep_method_id): Closes the window and updates the parent recipe instance.
        __del__(self): Destructor of the class that disconnects from the 'db_utils' object.

    Attributes
    ----------
        self.parent (Tk): The main window where the add method window will be displayed.
        self.recipe_instance (Recipe): The instance of the current recipe being edited.
        self.db_utils (DBUtils): An object handling the connection and queries to the database.
        self.cooking_method (tk.StringVar): Control variable for the name of the new cooking method.
    """
    def __init__(self, parent, recipe_instance) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.recipe_instance = recipe_instance

        self.db_utils = DBUtils()
        self.db_utils.connect()

        # TITULO
        parent.title('Pasos de Preparacion')
        # TAMAÑO DE LA VENTA
        parent.geometry('500x120')
        # DESACTIVA EL CAMBIO DE TAMAÑO
        parent.resizable(0, 0)
        parent.config(bg='#d9d9d9')

        # GUARDA EL PASO DE PREPARACION
        self.cooking_method = tk.StringVar()

        # GRID

        # ROWS
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=2)
        parent.rowconfigure(2, weight=1)

        #COLUMNS
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=2)
        parent.columnconfigure(2, weight=2)
        parent.columnconfigure(3, weight=1)

        # PASOS DE PREPARACION UI
        ttk.Label(self.parent, text="Paso de Preparacion:", padding=3).grid(
            row=0, column=1, sticky=tk.EW, columnspan=2
        )
        tk.Entry(self.parent, textvariable=self.cooking_method, justify=tk.RIGHT).grid(
            row=1, column=1, sticky=tk.EW, columnspan=2
        )
        # BOTONES: AGREGAR || CANCELAR
        ttk.Button(self.parent, text="Agregar", command=self.add_method).grid(
            row=2, column=1, padx=5, sticky=tk.EW)
        ttk.Button(self.parent, text="Cancelar", command=self.parent.destroy).grid(
            row=2, column=2, padx=5, sticky=tk.EW)
    
    def add_method(self) -> None:
        """Takes the data entered in the window and stores it in the database.

        This method is triggered when the 'Agregar' button is clicked.
        It retrieves the new cooking method from the user input, creates a new cooking method record in the database
        using the 'create_prep_method' method from the 'db_utils' object, and then calls 'close_window' to update
        the parent recipe instance and close the window.

        Raises
        ------
            Exception: If an error occurs during the database operation.
        """
        try:
            new_cooking_method = self.cooking_method.get()
            new_prep_method_id = self.db_utils.create_prep_method(new_cooking_method)
            self.close_window(new_cooking_method, new_prep_method_id)
        except Exception as e:
            msg.showerror(message=f'Error: {e}', title='Nuevo Paso', parent = self.parent)

    def close_window(self, new_prep_method: str, prep_method_id: int) -> None:
        """Closes the window and updates the parent recipe instance.

        This method is called after adding a new cooking method to the database successfully.
        It updates the 'recipe_instance' attributes related to the cooking method, such as 'prep_id' and 'prep_desc',
        with the data of the new cooking method. It also sets the 'add_flag' attribute to True to indicate that
        a new cooking method was added, and then closes the window.

        Parameters
        ----------
            new_prep_method (str): The name of the new cooking method.
            prep_method_id (int): The ID of the new cooking method in the database.
        """
        self.recipe_instance.prep_id = prep_method_id
        self.recipe_instance.prep_desc = new_prep_method
        self.recipe_instance.add_flag = True
        self.parent.destroy()

    def __del__(self):
        """Destructor of the class that disconnects from the database.

        This method is called when the class instance is no longer in use.
        It disconnects the 'db_utils' object from the database.
        """
        self.db_utils.disconnect()