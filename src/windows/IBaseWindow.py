from abc import ABC, abstractmethod
from src.utils.db_utils import DBUtils
import tkinter as tk
from tkinter import ttk

class IBaseWindow(ABC):
    """Abstract Base Class for creating a basic window with common configurations.

    This class defines a common set of methods and attributes for creating a basic window with common configurations.
    It serves as a base class for creating specific windows with customized user interfaces and functionalities.

    Parameters
    ----------
        parent (tk.Tk or tk.Toplevel): The parent window to which this window is associated.
        title (str): The title of the window.

    Attributes
    ----------
        parent (tk.Tk or tk.Toplevel): The parent window to which this window is associated.
        db_utils (DBUtils): An instance of the DBUtils class for database-related operations.

    Note
    ----
        Subclasses of this class must implement the `create_ui` method to create the specific user interface for the window.
    """
    def __init__(self, parent, title) -> None:
        super().__init__()
        self.parent = parent
        self.parent.title(title)
        self.parent.geometry('600x720')
        self.parent.config(bg='#d9d9d9')
        self.parent.resizable(0, 0)
        
        self.db_utils = DBUtils()
        self.db_utils.connect()

        # COLUMNS
        for i in range(7):
            self.parent.columnconfigure(i, weight=1)

        for i in range(8):
            if i != 2 and i != 4:
                self.parent.rowconfigure(i, weight=1)
            else:
                self.parent.rowconfigure(i, weight=2)

    @abstractmethod
    def create_ui(self):
        """Abstract method to create the user interface for the specific window.

        Subclasses must implement this method to create the customized user interface for the window.
        """
        pass
    
    def base_ui_config(self, btn_title: str) -> None:
        """Configure the base user interface elements for the recipe editor window.

        This method sets up the base user interface elements, such as labels, buttons, and entry fields, for the recipe editor window. It organizes the layout using the grid manager to create a structured display.

        Parameters
        ----------
            btn_title (str): The title to be displayed on the primary action button. Typically, it will be either 'Guardar' (Save) for adding a new recipe or 'Actualizar' (Update) for editing an existing recipe.
        """
        # NOMBRE DE LA RECETA
        ttk.Label(self.parent, text="Nombre:", padding=3).grid(row=0, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.name, justify=tk.RIGHT).grid(row=0, column=2, columnspan=4, sticky=tk.EW)

        # INGREDIENTES DE LA RECETA
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(row=1, column=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar Ingrediente", command=self.new_ingredient).grid(row=1, column=2, columnspan=2, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Eliminar Ingrediente", command=self.delete_ingredient).grid(row=1, column=4, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_ingredient_tree).grid(row=1, column=5, sticky=tk.EW, padx=5)

        # LISTA DE INGREDIENTES
        self.ingredient_list = self.create_treeview(2, 1, 1, ('Cantidad', 'Ingredientes'))
        self.load_ingredients()

        # PASOS DE LA RECETA
        ttk.Label(self.parent, text="Preparacion:", padding=3).grid(row=3, column=1, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar Paso", command=self.new_method).grid(row=3, column=2, columnspan=2, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Eliminar Paso", command=self.delete_method).grid(row=3, column=4, sticky=tk.EW, padx=5)
        ttk.Button(self.parent, text="Actualizar", command=self.refresh_method_tree).grid(row=3, column=5, sticky=tk.EW, padx=5)

        # LISTA DE INGREDIENTES
        self.method_list = self.create_treeview(4, 1, 0, ('Id', 'Pasos'))
        self.load_prep_methods()

        # TIEMPO DE PREPARACION
        ttk.Label(self.parent, text="Tiempo Preparacion (min):", padding=3).grid(row=5, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.preparation_time, justify= tk.RIGHT).grid(row=5, column=2, sticky=tk.EW)

        # TIEMPO DE COCCION
        ttk.Label(self.parent, text="Tiempo Cocción (min):", padding=3).grid(row=5, column=4,sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.cooking_time, justify= tk.RIGHT).grid(row=5, column=5, sticky=tk.EW)

        # Tags
        ttk.Label(self.parent, text="Etiquetas:", padding=3).grid(row=6, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.tags, justify=tk.RIGHT).grid(row=6, column=2, sticky=tk.EW)

        # Fav
        ttk.Label(self.parent, text="Favorita:", padding=3).grid(row=6, column=4, sticky=tk.EW)
        ttk.Combobox(self.parent, textvariable=self.favorite, values=['Si', 'No']).grid(row=6, column=5, sticky=tk.EW)

        # BOTONERA
        ttk.Button(self.parent, text=btn_title, command=self.save).grid(row=8, column=1, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)
        ttk.Button(self.parent, text="Cancelar", command=self.parent.destroy).grid(row=8, column=3, columnspan=3, sticky=tk.NSEW, padx=5, pady=5)

    def create_treeview(self, tree_row, tree_column, option, columns_value) -> ttk.Treeview:
        """Create and configure a Treeview widget.

        This method creates a new instance of a Treeview widget and configures its appearance and behavior based on theprovided parameters.

        Parameters
        ----------
            tree_row (int): The row in the grid where the Treeview should be placed.
            tree_column (int): The column in the grid where the Treeview should be placed.
            option (int): The option to choose the Treeview's layout. If 1, it configures the Treeview for displaying ingredient information. Otherwise, it configures it for displaying preparation methods.
            columns_value (tuple): A tuple containing the column names to be displayed in the Treeview headings.

        Returns
        -------
            ttk.Treeview: The configured Treeview widget.

        Note
        ----
            When `option` is 1, the Treeview is configured for displaying ingredient information with columns 'Cantidad' and 'Ingredientes'. When `option` is not 1, the Treeview is configured for displaying preparation methods with columns 'Id' and 'Pasos'.
        """
        tree = ttk.Treeview(self.parent, columns=columns_value, show='headings',  height=5)

        tree.grid(row=tree_row, column=tree_column, sticky=(tk.NSEW), padx=5, columnspan=5 )

        if option == 1:
            tree.heading('Cantidad', text='Cantidad')
            tree.column(0, anchor=tk.CENTER, stretch=tk.NO, width=120)
            tree.heading('Ingredientes', text='Ingredientes')
            tree.column(1)
        else:
            tree.heading('Id', text='Id')
            tree.column(0, anchor=tk.CENTER, stretch=tk.NO, width=40)
            tree.heading('Pasos', text='Pasos')

        return tree
