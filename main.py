import tkinter as tk
from tkinter import ttk
from src.windows.NewRecipe import *
from src.windows.ReadRecipe import ReadRecipe
from src.windows.EditRecipe import EditRecipe
import os
from datetime import datetime
import random
from src.utils.db_utils import DBUtils


class App(ttk.Frame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.search_option = tk.StringVar()
        self.search_input = tk.StringVar()
        
        self.edited_row = None
        self.edit_flag = False
        
        self.added_row = None
        self.new_flag = False
        
        self.treeview_content = []

        self.db_utils = DBUtils()
        self.db_utils.connect()

        # MAIN WINDOW
        parent.geometry('1280x720')
        parent.title('Kitchen App')
        parent.resizable(0, 0)
        parent.config(bg='#d9d9d9')
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Add the rowheight
        self.style.configure('Treeview', rowheight=30)

        # BUTTONS
        self.set_ui()

        # COLUMNS
        for i in range(5):
            if i == 0:
                parent.columnconfigure(i, weight=4)
            else:
                parent.columnconfigure(i, weight=1)

        # ROWS
        for i in range(6):
            if i == 0:
                parent.rowconfigure(i, weight=1)
            else:
                parent.rowconfigure(i, weight=7)

        self.tree = self.create_tree()
        self.read_data()

    def set_ui(self) -> None:
        """Sets up the user interface for managing recipes.

        This method creates and configures the buttons and input elements required to
        perform CRUD (Create, Read, Update, Delete) operations on recipes. It also adds
        elements for searching and refreshing the recipe list.

        Buttons:
            - "Nueva": Opens a new window to create a new recipe.
            - "Editar": Opens a new window to edit an existing recipe.
            - "Ver": Opens a new window to view the details of a recipe.
            - "Eliminar": Deletes the selected recipe from the database.
            - "Actualizar": Refreshes the displayed recipe list in the treeview.

        This method is typically called during the initialization of the main window to
        set up the user interface for managing recipes.
        """
        # CREAR NUEVA RECETA
        ttk.Button(self.parent, text="Nueva", command=self.new_recipe).grid(
            row=1, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # EDITAR RECETA EXISTENTE
        ttk.Button(self.parent, text="Editar", command=self.edit_recipe).grid(
            row=2, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # VER UNA RECETA
        ttk.Button(self.parent, text="Ver", command=self.read_recipe).grid(
            row=3, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # ELIMINAR UNA RECETA
        ttk.Button(self.parent, text="Eliminar", command=self.delete_recipe).grid(
            row=4, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        # ACTUALIZAR TREEVIEW
        ttk.Button(self.parent, text="Actualizar", command=self.recover_treeview_data).grid(
            row=5, column=0, padx=10, pady=5, sticky=(tk.NSEW))
        
        ttk.Combobox(self.parent, textvariable=self.search_option, 
            values=['Nombre', 'Etiquetas', 'Tiempo de Preparacion', 'Ingredientes'], justify=tk.RIGHT).grid(row=0, column=1, padx=10, pady=5, sticky=tk.NSEW)
        ttk.Entry(self.parent, textvariable=self.search_input, justify=tk.RIGHT).grid(
            row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)
        ttk.Button(self.parent, text="Buscar", command=self.search).grid(
            row=0, column=3, padx=10, pady=5, sticky=(tk.NSEW))
        ttk.Button(self.parent, text="Reset", command=self.recover_treeview_data).grid(
            row=0, column=4, padx=10, pady=5, sticky=(tk.NSEW))

    def create_tree(self) -> ttk.Treeview:
        """Creates and configures a Treeview widget for displaying recipe information.

        This method creates a Treeview widget with specified columns to display the details
        of recipes in a tabular format. The widget is set up to show only the headings at
        the top and to display data in multiple columns.

        Columns:
            - 'ID': The unique identifier of the recipe.
            - 'Nombre': The name of the recipe.
            - 'Ingredientes': A summary of the recipe's ingredients.
            - 'Tiempo de Preparacion': The preparation time of the recipe.
            - 'Tiempo de Coccion': The cooking time of the recipe.
            - 'Creado': The creation date of the recipe.

        The Treeview is set up to display the data in the following layout:
        | ID | Nombre | Ingredientes | Tiempo de Preparacion | Tiempo de Coccion | Creado |

        The column widths are adjusted to ensure the information is presented clearly.

        The Treeview is also equipped with a vertical scrollbar to navigate through the
        recipe list when there are more entries than the widget can display.

        Returns
        -------
            ttk.Treeview: The configured Treeview widget for displaying recipe information.

        Note
        ----
            This method is typically called during the initialization of the main window to
            create and set up the recipe list display.
        """
        # NUMERO DE COLUMNAS Y NOMBRES
        columns = ('ID', 'Nombre', 'Ingredientes', 'Tiempo de Preparacion', 'Tiempo de Coccion', 'Creado')
        # CREA EL WIDGET
        tree = ttk.Treeview(self.parent, columns=columns, show='headings')
        # INSERTARLO EN LA GRILLA
        tree.grid(row=1, column=1, sticky=(tk.NSEW), pady=10, padx=5, columnspan=4, rowspan=5)
        # INSERTAR EL ENCABEZADO
        #ID
        tree.heading('ID', text='ID')
        tree.column(0, anchor=tk.CENTER, stretch=tk.NO, width=40)
        #NOMBRE
        tree.heading('Nombre', text='Nombre')
        tree.column(1, anchor=tk.CENTER)
        #INGREDIENTES
        tree.heading('Ingredientes', text='Ingredientes')
        tree.column(2, anchor=tk.CENTER, stretch=tk.NO, width=350)
        #TIEMPO DE PREPARACION
        tree.heading('Tiempo de Preparacion', text='Tiempo de Preparacion')
        tree.column(3, anchor=tk.CENTER, stretch=tk.NO, width=140)
        #TIEMPO DE COCCION
        tree.heading('Tiempo de Coccion', text='Tiempo de Coccion')
        tree.column(4, anchor=tk.CENTER, stretch=tk.NO, width=140)
        #CREADO EN
        tree.heading('Creado', text='Creado')
        tree.column(5, anchor=tk.CENTER, stretch=tk.NO, width=140)

        # AGREGAR SCROLLBAR
        scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=5, sticky=tk.NS, pady=10, rowspan=5)

        return tree

    def read_data(self) -> None:
        """Reads recipe data from the database and populates the Treeview.

        This method retrieves the recipe data from the database using the `db_utils` object
        and populates the Treeview widget with the retrieved data. The Treeview should be
        already created using the `create_tree` method before calling this function.

        The retrieved data includes the ID, name, ingredients, preparation time, cooking
        time, and creation date for each recipe. The data is formatted appropriately before
        being inserted into the Treeview.
        """
        self.recipe_list = self.db_utils.read_recipes()
        for recipe in self.recipe_list:
            data = [recipe[0], recipe[1], recipe[5], f'{recipe[2]} min', f'{recipe[3]} min', recipe[4]]
            self.tree.insert('', tk.END, values= data)

    #CRUD
    def new_recipe(self) -> None:
        """Opens a new window for adding a new recipe.

        This method creates a new top-level window (`Toplevel`) to display a form for adding
        a new recipe.

        The `NewRecipe` class, representing the window for adding a new recipe, is
        instantiated and displayed as a modal window using `wait_window`, ensuring that the
        main window remains inactive until the user finishes interacting with the
        `NewRecipe` window.

        If a new recipe is successfully added (`new_flag` is set to `True`), the method
        formats the recipe data and inserts it into the Treeview.

        Note:
            The `NewRecipe` window should handle the actual saving of the new recipe data.

        Raises:
            Exception: If an error occurs while adding a new recipe, an error message is
            displayed using the `msg.showerror` function.
        """
        try:
            toplevel = tk.Toplevel(self.parent)
            new_recipe_window = NewRecipe(toplevel, 'Agregar Receta', self).grid()
            toplevel.wait_window(new_recipe_window)
            if self.new_flag:
                ingredients = ''
                for ingredient_details in self.added_row['ingredients']:
                    ingredients += f'{ingredient_details[1]},'
                new_value = (
                    self.added_row['id'],
                    self.added_row['name'],
                    ingredients[:-1],
                    f"{self.added_row['prep_time']} min",
                    f"{self.added_row['cook_time']} min",
                    self.added_row['created_at']
                )
                self.tree.insert('', tk.END, values=new_value)
                self.new_flag = False
        except Exception as e:
            msg.showerror(message=f'Error: {e}', title='Nueva Receta', parent = self.parent)

    def edit_recipe(self) -> None:
        """Opens a window to edit the selected recipe and updates the recipe list.

        This method is triggered when the user clicks the 'Edit Recipe' button. It opens
        a new window to allow the user to edit the details of the selected recipe. After
        editing, the recipe list is updated with the new values.

        Raises
        ------
            IndexError: If no recipe item is selected before clicking the 'Edit Recipe'
            button, this exception is raised, and an error message is shown to the user.
        """
        try:
            item = self.get_recipe_id()
            id = item[0]
            row = item[1]
            toplevel = tk.Toplevel(self.parent)
            edit_window = EditRecipe(toplevel, 'Editar Receta', id, self).grid()
            toplevel.wait_window(edit_window)
            if self.edit_flag:
                new_value = (
                    id, 
                    self.edited_row[0], 
                    self.edited_row[1], 
                    f'{self.edited_row[2]} min', 
                    f'{self.edited_row[3]} min', 
                    self.tree.item(row)['values'][5]
                )
                self.tree.item(row, values=new_value)
                self.edit_flag = False
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Editar Receta', parent = self.parent)

    def delete_recipe(self) -> None:
        """Deletes the selected recipe from the database and refreshes the recipe list.

        This method is triggered when the user clicks the 'Delete Recipe' button. It
        retrieves the selected recipe's ID, deletes the recipe from the database, and then
        refreshes the recipe list to reflect the changes.

        Raises
        ------
            IndexError: If no recipe item is selected before clicking the 'Delete Recipe'
            button, this exception is raised, and an error message is shown to the user.
        """
        try:
            select_item = self.get_recipe_id()
            self.db_utils.delete_recipe(select_item[0])
            self.refresh_recipe_tree()
            msg.showinfo(message='Receta eliminada con exito, actualice la lista', title='Eliminar Receta', parent = self.parent)
        except IndexError:
            msg.showerror(message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Eliminar Receta', parent=self.parent)
    
    def read_recipe(self) -> None:
        """Displays the details of the selected recipe in a new window.

        This method is triggered when the user clicks the 'Read Recipe' button. It opens
        a new window and displays the details of the selected recipe, such as its
        ingredients and cooking instructions.

        Raises:
            IndexError: If no recipe item is selected before clicking the 'Read Recipe'
            button, this exception is raised, and an error message is shown to the user.
        """
        try: 
            item = self.get_recipe_id()
            id = item[0]
            toplevel = tk.Toplevel(self.parent)
            ReadRecipe(toplevel, 'Leer Receta', id).grid()
        except IndexError:
            msg.showerror(
                message='No ha seleccionado ningun item, haga click sobre un item y presione el boton.', title='Ver Receta', parent=self.parent)

    def refresh_recipe_tree(self) -> None:
        """Refreshes the recipe list in the Treeview widget.

        This method updates the recipe list displayed in the Treeview widget. It clears
        the existing content of the widget, creates a new Treeview, and then reads the
        data from the database to populate the widget with up-to-date recipe information.
        """
        self.tree.delete(*self.tree.get_children())
        self.tree = self.create_tree()
        self.read_data()

    def recover_treeview_data(self):
        """Recovers and displays the previously stored treeview data.

        This method checks if there is any previously stored content for the Treeview
        widget. If there is no stored data, it displays a message to inform the user
        that the recipe book is up to date. Otherwise, it clears the existing content of
        the Treeview, and then populates it with the previously stored data.
        """
        if len(self.treeview_content) == 0:
            msg.showinfo(
                message='El recetario esta al dia', title='Recetas', parent=self.parent)
        else:
            self.tree.delete(*self.tree.get_children())
            for recipe in self.treeview_content:
                self.tree.insert('', tk.END, values=recipe)
            self.treeview_content = []

    def save_treeview(self):
        """Saves the content of the Treeview widget to a temporary storage.

        This method iterates through all the items in the Treeview widget and saves their
        recipe details to a temporary storage list called 'treeview_content'. The stored
        content can later be used for recovery or other purposes.
        """
        for item in self.tree.get_children():
            recipe = self.tree.item(item, "values")
            self.treeview_content.append(recipe)

    def get_recipe_id(self) -> int:
        """Retrieves the ID of the selected recipe and its associated Treeview item.

        This method gets the ID of the selected recipe and the associated Treeview item
        that represents the recipe. It is typically used when performing operations on a
        specific recipe, such as editing or deleting it.

        Returns
        -------
            int: The ID of the selected recipe.
        """
        select_item = self.tree.focus()
        return self.tree.item(select_item)['values'][0], select_item

    def search(self) -> None:
        """Performs a search based on the selected option.

        This method retrieves the selected search option and the input value from the
        corresponding input fields. Based on the chosen search option, it initiates a
        search operation to find recipes that match the specified criteria.

        The search options include 'Nombre' (Name), 'Etiquetas' (Tags), 'Tiempo de
        Preparacion' (Preparation Time), and 'Ingredientes' (Ingredients).

        If an invalid search option is selected, an error message is displayed.
        """
        option = self.search_option.get()
        search_in = self.search_input.get()
        if option == 'Nombre':
            self.search_by_name(search_in)
        elif option == 'Etiquetas':
            self.search_by_tags(search_in)
        elif option == 'Tiempo de Preparacion':
            self.search_by_prep_time(search_in)
        elif option == 'Ingredientes':
            self.search_by_ingredients(search_in)
        else:
            msg.showerror(title='Buscar', message='Error! Escoja una opcion valida')

    def read_search_data(self, recipes: list) -> None:
        """Displays search results in the Treeview widget.

        This method is responsible for displaying the search results in the Treeview
        widget. It takes a list of recipes as input and populates the Treeview with the
        relevant recipe data.

        Parameters
        ----------
            recipes (list): A list of recipes retrieved from the database that match the
            search criteria.
        """
        if len(recipes) != 0:
            self.tree = self.create_tree()
            for recipe in recipes:
                data = [recipe[0], recipe[1], recipe[5], f'{recipe[2]} min', f'{recipe[3]} min', recipe[4]]
                self.tree.insert('', tk.END, values=data)
        else:
            msg.showwarning(
                title='Buscar', message='No se ha encontrado coincidencias', parent=self.parent)

    def search_by_name(self, name: str) -> None:
        """Searches recipes by name and displays the results.

        This method performs a search for recipes by name. It takes the input 'name'
        as the search keyword and queries the database for recipes that match the
        specified name. The search results are then displayed in the Treeview widget.

        Parameters
        ----------
            name (str): The name of the recipe to search for.
        """
        self.db_utils.disconnect()
        self.db_utils.connect()
        self.save_treeview()
        found_recipes = self.db_utils.search_by_name(name)
        self.read_search_data(found_recipes)

    def search_by_tags(self, tags: str) -> None:
        """Searches recipes by tags and displays the results.

        This method performs a search for recipes by tags. It takes the input 'tags'
        as the search keyword and queries the database for recipes that have matching
        tags. The search results are then displayed in the Treeview widget.

        Parameters
        ----------
            tags (str): The tags to search for.
        """
        self.db_utils.disconnect()
        self.db_utils.connect()
        self.save_treeview()
        found_recipes  = self.db_utils.search_by_tags(tags)
        self.read_search_data(found_recipes)

    def search_by_prep_time(self, prep_time: str) -> None:
        """Searches recipes by preparation time and displays the results.

        This method performs a search for recipes by preparation time. It takes the
        input 'prep_time' as the search keyword and queries the database for recipes
        that have matching preparation times. The search results are then displayed
        in the Treeview widget.

        Parameters
        ----------
            prep_time (str): The preparation time to search for. It should be a string
            representing the preparation time in minutes.
        """
        self.db_utils.disconnect()
        self.db_utils.connect()
        self.save_treeview()
        found_recipes = self.db_utils.search_by_prep_time(prep_time)
        self.read_search_data(found_recipes)

    def search_by_ingredients(self, ingredients: str) -> None:
        """Searches recipes by ingredients and displays the results.

        This method performs a search for recipes by ingredients. It takes the input
        'ingredients' as the search keyword and queries the database for recipes that
        contain the specified ingredients. The search results are then displayed in
        the Treeview widget.

        Parameters
        ----------
            ingredients (str): The ingredients to search for.
        """
        self.db_utils.disconnect()
        self.db_utils.connect()
        self.save_treeview()
        found_recipes = self.db_utils.search_by_ingredient(ingredients)
        self.read_search_data(found_recipes)

    def __del__(self):
        """Destructor method to disconnect from the database.

        This special method is automatically called when the instance of the class is
        being deleted. It ensures that the connection to the database is properly
        closed and resources are released.
        """
        self.db_utils.disconnect()


root = tk.Tk()
App(root).grid()
root.mainloop()
