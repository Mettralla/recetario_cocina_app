import tkinter as tk
from tkinter import ttk
import csv

METHOD_LIST = "./csv_files/method_list_temp.csv"

class AddMethod(ttk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent, padding=(20))
        self.parent = parent

        parent.title('Pasos de Preparacion')
        parent.geometry('500x120')
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
    
    def get_last_id(self):
        with open(METHOD_LIST, 'r') as csvfile:
            reader = csvfile.readlines()
            last_id = reader[-1].split(',')[0]
        if last_id == 'id':
            return 0
        else:
            return int(last_id)
    
    def add_method(self):
        new_cooking_method = {"id": self.get_last_id() + 1, "paso": self.cooking_method.get()}
        campos = ["id", "paso"]
        with open(METHOD_LIST, 'a', newline="\n") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=campos)
            writer.writerow(
                {
                    "id": new_cooking_method['id'], "paso": new_cooking_method['paso']
                }
            )
        self.parent.destroy()
