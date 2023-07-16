import tkinter as tk
from tkinter import ttk
import csv
from modules.globalVar import RECIPE_LIST
from src.windows.IBaseWindow import *
from PIL import ImageTk, Image

class ReadRecipe(ttk.Frame, IBaseWindow):
    def __init__(self, parent, title: str, recipe_id: str) -> None:
        ttk.Frame.__init__(self, parent, padding=(20))
        IBaseWindow.__init__(self, parent, title)

        self.id = recipe_id
        self.recipe = self.get_recipe()
        self.star = ImageTk.PhotoImage(
            Image.open('images\star.png').resize((30, 30)))
        self.empty_star = ImageTk.PhotoImage(
            Image.open('images\empty_star.png').resize((30, 30)))

        self.create_ui()


    def get_recipe(self) -> dict:
        '''Lee el fichero, identifica la receta a traves del id y la convierte en un diccionario lista para ser mostrada'''
        selected_recipe = {}
        with open(RECIPE_LIST, "r", newline="\n") as csvfile:
            reader = csv.reader(csvfile)
            for recipe in reader:
                try:
                    if int(recipe[0]) == self.id:
                        selected_recipe = {
                            'id': recipe[0],
                            'nombre': recipe[1],
                            'ingredientes': recipe[2],
                            'cantidades': recipe[3],
                            'preparacion': recipe[4],
                            'tiempo de preparacion': recipe[5],
                            'tiempo de coccion': recipe[6],
                            'creado': recipe[7],
                            'imagen': recipe[8],
                            'etiquetas': recipe[9],
                            'favorito': recipe[10]
                        }
                    else: 
                        pass
                except ValueError:
                        pass
        return selected_recipe

    def create_ui(self) -> None:
        '''Muestra la receta'''
        # TITULO
        if self.recipe['favorito'] == 'Si':
            ttk.Label(self.parent, text=self.recipe['nombre'], font=(
                'Arial', 25), image=self.star, compound=tk.LEFT, justify=tk.LEFT).grid(row=0, column=1)
        else: 
            ttk.Label(self.parent, text=self.recipe['nombre'], font=(
                'Arial', 25), image=self.empty_star, compound=tk.LEFT, justify=tk.LEFT).grid(row=0, column=1)
        
        # IMAGEN
        if self.recipe['imagen'] != 'None':
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
        ttk.Label(self.parent, text=f"Tiempo de Preparacion: {self.recipe['tiempo de preparacion']}", padding=3).grid(
            row=5, column=1, columnspan=3, sticky=tk.EW)
        
        # TIEMPO DE COCCION
        ttk.Label(self.parent, text=f"Tiempo de Cocción: {self.recipe['tiempo de coccion']}", padding=3).grid(
            row=5, column=3, columnspan=3, sticky=tk.EW)
        
        ttk.Label(self.parent, text=f"Etiquetas: {self.recipe['etiquetas']}", padding=3).grid(
            row=6, column=1, columnspan=5, sticky=tk.EW)
        
        # BOTON
        ttk.Button(self.parent, text="Cerrar", command=self.parent.destroy).grid(
            row=7, column=1, columnspan=5, sticky=tk.NSEW, padx=5, pady=5)

    def load_ingredients(self) -> None:
        '''Carga los ingredientes de la lista en el Treeview'''
        ingredients = self.recipe['ingredientes'].split(',')
        amounts = self.recipe['cantidades'].split(',')
        for i in range(len(ingredients)):
            self.ingredient_list.insert(
                '', tk.END, values=[amounts[i], ingredients[i]])

    def load_method_list(self) -> None:
        '''Carga los pasos de preparacion en la lista'''
        prep_methods = self.recipe['preparacion'].split(',')
        # print(prep_methods)
        for index, prep_method in enumerate(prep_methods, 1):
            prep_value = prep_method.strip()
            self.method_list.insert(
                '', tk.END, values=[index, prep_value]
            )
