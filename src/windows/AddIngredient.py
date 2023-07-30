import tkinter as tk
from tkinter import ttk
from src.utils.db_utils import DBUtils
from tkinter import messagebox as msg

class AddIngredient(ttk.Frame):
    '''Clase que representa la ventana de agregar ingrediente individual'''
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

    def close_window(self, ingredient_value, new_ingredient):
        self.recipe_instance.ingredient_value = ingredient_value
        self.recipe_instance.data_ing = (str(new_ingredient['cantidad']) + ' ' + new_ingredient['medida'], new_ingredient['nombre'])
        self.recipe_instance.add_flag = True
        self.parent.destroy()

    def __del__(self):
        self.db_utils.disconnect()
