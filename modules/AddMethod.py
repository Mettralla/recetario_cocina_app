import tkinter as tk
from tkinter import ttk
import csv

METHOD_LIST = "./csv_files/method_list_temp.csv"

class AddMethod(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent
        self.num = 1

        parent.title('Ingredientes')
        parent.geometry('200x150')
        parent.resizable(0, 0)

        self.cooking_method = tk.StringVar()

        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=2)
        parent.rowconfigure(2, weight=1)
        
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=2)
        parent.columnconfigure(2, weight=2)
        parent.columnconfigure(3, weight=1)

        ttk.Label(self.parent, text="Paso de Preparacion:", padding=3).grid(
            row=0, column=1, sticky=tk.EW, columnspan=2
        )
        tk.Entry(self.parent, textvariable=self.cooking_method).grid(
            row=1, column=1, sticky=tk.EW, columnspan=2
        )
        
        ttk.Button(self.parent, text="Agregar", command=self.add_method).grid(
            row=2, column=1, padx=5, sticky=tk.EW)
        ttk.Button(self.parent, text="Cancelar", command=self.parent.destroy).grid(
            row=2, column=2, padx=5, sticky=tk.EW)
    
    def add_method(self):
        pass
        # new_cooking_method = {"numero": self.num, "paso": text_method}
        # campos = ["numero", "paso"]
        # with open(METHOD_LIST, 'a') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=campos)
        #     writer.writerow(
        #         {
        #             "numero": new_cooking_method['numero'], "paso": new_cooking_method['paso']
        #         }
        #     )
        # self.parent.destroy()
