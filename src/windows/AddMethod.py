import tkinter as tk
from tkinter import ttk
from src.utils.db_utils import DBUtils
from tkinter import messagebox as msg

class AddMethod(ttk.Frame):
    '''Clase que representa a la ventana de agregar nuevo paso de preparacion'''
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
        '''Toma los datos ingresados en la ventana y los almacena en la base de datos'''
        try:
            new_cooking_method = self.cooking_method.get()
            new_prep_method_id = self.db_utils.create_prep_method(new_cooking_method)
            self.close_window(new_cooking_method, new_prep_method_id)
        except Exception as e:
            msg.showerror(message=f'Error: {e}', title='Nuevo Paso', parent = self.parent)

    def close_window(self, new_prep_method, prep_method_id):
        self.recipe_instance.prep_id = prep_method_id
        self.recipe_instance.prep_desc = new_prep_method
        self.recipe_instance.add_flag = True
        self.parent.destroy()

    def __del__(self):
        self.db_utils.disconnect()