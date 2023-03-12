import tkinter as tk
from tkinter import ttk
import csv

class AddIngrediente(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent

        parent.title('Ingredientes')
        parent.geometry('250x120')
        parent.resizable(0, 0)

        self.ingrediente = tk.StringVar()
        self.cantidad = tk.IntVar()
        self.medida = tk.StringVar()
        self.medidas = ['miligramos', 'gramos', 'kilogramos',
                        'cucharadas', 'cucharaditas', 'unidades']

        # COLUMNS
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(2, weight=1)
        parent.columnconfigure(3, weight=1)

        # ROWS
        parent.rowconfigure(0, weight=1)  # Name
        parent.rowconfigure(1, weight=2)  # Ingredients
        parent.rowconfigure(2, weight=2)  # Ingred list
        parent.rowconfigure(3, weight=1)  # Prep

        # INGREDIENTES
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(
            row=0, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.ingrediente).grid(
            row=0, column=2, sticky=tk.EW)
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(
            row=1, column=1, sticky=tk.EW)
        ttk.Entry(self.parent, textvariable=self.cantidad, justify='right').grid(
            row=1, column=2, sticky=tk.EW, padx=5)
        ttk.Label(self.parent, text="Ingredientes:", padding=3).grid(
            row=2, column=1, sticky=tk.EW)
        ttk.Combobox(self.parent, textvariable=self.medida, values=self.medidas).grid(
            row=2, column=2, sticky=tk.EW)
        ttk.Button(self.parent, text="Agregar", command=self.add_ingredient).grid(
            row=3, column=0, padx=5, columnspan=2, sticky=tk.EW)
        ttk.Button(self.parent, text="Cancelar", command=self.parent.destroy).grid(
            row=3, column=2, padx=5, columnspan=2, sticky=tk.EW)

    def add_ingredient(self):
        new_ingredient = {"nombre": self.ingrediente.get(
        ), "cantidad": self.cantidad.get(), "medida": self.medida.get()}
        campos = ["nombre", "cantidad", "medida"]
        with open("./csv_files/ingredients_temp.csv", 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writerow(
                {
                    "nombre": new_ingredient['nombre'], "cantidad": new_ingredient['cantidad'], "medida": new_ingredient['medida']
                }
            )
        self.parent.destroy()
