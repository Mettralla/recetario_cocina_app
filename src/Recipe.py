from src.Ingredient import Ingredient
from datetime import datetime
import shutil
from modules.globalVar import DESTINATION
from tkinter import messagebox as msg


class Recipe():
    '''La clase representa a una receta de cocina.
        params:
            (int) id: id de la receta
            (str) name: nombre de la receta
            (list) ingredients: lista de ingredientes, contiene nombre, cantidad, medida
            (list) preparation: pasos de preparacion
            (int) preparation_time: tiempo de preparacion en minutos
            (int) cooking_time: tiempo de coccion en minutos
            (str) tags: las etiquetas de la receta
            (str) favorite: Si la receta es favorita o no
            (datetime) created_at: fecha y hora de creacion
    '''

    def __init__(self, id: int, name: str, ingredients: list[Ingredient], preparation: list[str], preparation_time: int, cooking_time: int, tags: str, favorite: str, created_at=datetime.now(), image: str = None) -> None:
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.preparation = preparation
        self.preparation_time = preparation_time
        self.cooking_time = cooking_time
        self.created_at = created_at
        self.image = image
        self.tags = tags
        self.favorite = favorite

    def get_id(self) -> str:
        '''Transforma el id en string y lo devuelve'''
        return str(self.id)

    def get_name(self) -> str:
        '''Regresa el nombre'''
        return self.name

    def get_ingredients(self) -> str:
        '''Transforma la lista de ingredientes en string y la devuelve'''
        ingredient_list = ''
        for ingredient in self.ingredients:
            ingredient_list += ingredient.get_name()
            if self.ingredients[-1] != ingredient:
                ingredient_list += ','
        return ingredient_list.lower()

    def get_amounts(self) -> str:
        '''Transforma la lista de cantidades y metricas en string y la devuelve'''
        amounts_list = ''
        for ingredient in self.ingredients:
            amounts_list += ingredient.get_amount()
            if self.ingredients[-1] != ingredient:
                amounts_list += ','
        return amounts_list

    def get_preparation(self) -> str:
        '''Transforma la lista de pasos preparacion en string y la devuelve'''
        return ','.join(self.preparation)

    def get_prep_time(self) -> str:
        '''Regresa el tiempo de preparacion expresada en minuto'''
        return f'{str(self.preparation_time)} min'

    def get_cooking_time(self) -> str:
        '''Regresa el tiempo de coccion expresada en minuto'''
        return f'{str(self.cooking_time)} min'

    def get_created_at(self) -> str:
        '''Regresa el tiempo de creacion'''
        return self.created_at.strftime("%H:%M %d-%m-%Y")

    def get_source(self) -> str:
        '''Copia la imagen a la carpeta de imagenes y devuelve el ruta'''
        try:
            if self.image != None:
                shutil.copy(self.image, DESTINATION)
                img_name = self.image.split('/')[-1]
                return "images\\" + img_name  # CORREGIR FORMATO
            else:
                return 'None'
        except:
            msg.showerror(
                message='Un error sucedio durante la creacion de la imagen', title='Agregar Imagen')

    def get_tags(self) -> str:
        '''Regresa las etiquetas de la receta'''
        return(self.tags)

    def get_favorite(self) -> bool:
        '''Regresa si es favorita o no'''
        return self.favorite 

    def format_values(self) -> dict[str]:
        '''Toma todos los valores y regresa en un diccionario de strings, listo para insertarse en un csv'''
        dict_recipe = {
            'id': self.get_id(),
            'nombre': self.get_name(),
            'ingredientes': self.get_ingredients(),
            'cantidades': self.get_amounts(),
            'preparacion': self.get_preparation(),
            'tiempo de preparacion': self.get_prep_time(),
            'tiempo de coccion': self.get_cooking_time(),
            'creado': self.get_created_at(),
            'imagen': self.get_source(),
            'etiquetas': self.get_tags(),
            'favorito': self.get_favorite()
        }
        return dict_recipe
