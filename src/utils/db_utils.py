# from db_config import DB_CONFIG
from src.utils.db_config import DB_CONFIG
import mysql.connector
from datetime import date
import random


class DBUtils:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(**DB_CONFIG)

    def disconnect(self):
        if self.connection:
            self.connection.close()

# INGREDIENTS CRUD -------------------------------------------------

    def create_ingredient(self, ingredient_name) -> int:
        cursor = self.connection.cursor()
        try:
            existing_ingredient_id = self.check_record_existence(ingredient_name, 'ingredientes')
            if existing_ingredient_id is None:
                query = "INSERT INTO ingredientes (nombre) VALUES (%s)"
                values = (ingredient_name,)
                cursor.execute(query, values)
                self.connection.commit()
                
                cursor.execute("SELECT LAST_INSERT_ID()")
                return cursor.fetchone()[0]
            else:
                return existing_ingredient_id
        finally:
            cursor.close()
    
    def read_ingredients(self, ingredients_recipe_ids: int):
        cursor = self.connection.cursor()
        print(f"read_ingredients - ingredient_ids: {ingredients_recipe_ids}")
        ingredients_data = []
        try:
            for id in ingredients_recipe_ids:
                print(f"read_ingredients - id: {id}")
                query = f"""SELECT ingredientes.nombre, ingredientes_receta.cantidad, ingredientes_receta.medida 
                        FROM ingredientes JOIN ingredientes_receta
                        ON ingredientes_receta.id_ingrediente = ingredientes.id_ingrediente
                        WHERE ingredientes_receta.id_ingredientes_receta = {id}"""
                cursor.execute(query)
                ingredient = cursor.fetchall()
                print(f"read_ingredients - ingredient: {ingredient}")
                ingredients_data.extend(ingredient)
            return ingredients_data
        finally:
            print(f"read_ingredients - data: {ingredients_data}")
            cursor.close()

# INGREDIENTS_RECIPE ---------------------------------

    def add_ingredient_to_recipe(self, ingredient_id: int, amount: int, units: str) -> int:
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO ingredientes_receta (id_ingrediente, cantidad, medida) VALUES (%s, %s, %s)"
            values = (ingredient_id, amount, units)
            cursor.execute(query, values)
            self.connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def add_recipe_id_to_ingredients(self, ingredient_recipe_id, recipe_id):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE ingredientes_receta SET id_receta = %s WHERE id_ingredientes_receta = %s"
            values = (recipe_id, ingredient_recipe_id)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

    def delete_ingredient_to_recipe(self, ingredient_recipe_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM ingredientes_receta WHERE id_ingredientes_receta = %s"
            values = (ingredient_recipe_id,)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

    def check_record_existence(self, name, table):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {table} WHERE nombre = %s"
        values = (name,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result if result == None else result[0]

# PREP METHODS CRUD -------------------------------------------------

    def create_prep_method(self, prep_method_description: str) -> int:
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO pasos (descripcion) VALUES (%s)"
            values = (prep_method_description,)
            cursor.execute(query, values)
            self.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def delete_prep_method(self, prep_method_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM pasos WHERE id_paso = %s"
            values = (prep_method_id,)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

# PREP_METHOD_RECIPE ---------------------------------

    def add_prep_method_to_recipe(self, prep_method_id: int, order: int, recipe_id: int):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO pasos_receta (id_paso, id_receta, orden) VALUES (%s, %s, %s)"
            values = (prep_method_id, recipe_id, order)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

# RECIPE -----------------------------------------

    def create_recipe(self, new_recipe):
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO recetas (nombre, tiempo_preparacion, tiempo_coccion, imagen, favorito) VALUES (%s, %s, %s, %s, %s)"
            values = (
                new_recipe['name'],
                new_recipe['prep_time'],
                new_recipe['cook_time'],
                new_recipe['image'],
                new_recipe['favorite']
            )
            cursor.execute(query, values)
            self.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def read_recipes(self):
        try:
            cursor = self.connection.cursor()
            query = """
                    SELECT recetas.id_receta, recetas.nombre, recetas.tiempo_preparacion, recetas.tiempo_coccion, recetas.creado_el,
                    (
                        SELECT GROUP_CONCAT(ingredientes.nombre SEPARATOR ',')
                        FROM ingredientes
                        JOIN ingredientes_receta
                        ON ingredientes.id_ingrediente = ingredientes_receta.id_ingrediente
                        WHERE ingredientes_receta.id_receta = recetas.id_receta
                    ) AS ingredientes
                    FROM
                        recetas;"""
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()

    def get_recipe_by_id(self, recipe_id):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT
                    recetas.id_receta, recetas.nombre, recetas.tiempo_preparacion, 
                    recetas.tiempo_coccion, recetas.imagen, recetas.favorito,
                    (
                        SELECT GROUP_CONCAT(ingredientes.nombre, ' (', ingredientes_receta.cantidad, ' ', ingredientes_receta.medida, ')' SEPARATOR ',')
                        FROM ingredientes JOIN ingredientes_receta
                        ON ingredientes.id_ingrediente = ingredientes_receta.id_ingrediente
                        WHERE ingredientes_receta.id_receta = recetas.id_receta
                    ) AS ingredientes,
                    (
                        SELECT GROUP_CONCAT(pasos.descripcion SEPARATOR ',')
                        FROM pasos JOIN pasos_receta
                        ON pasos.id_paso = pasos_receta.id_paso
                        WHERE pasos_receta.id_receta = recetas.id_receta
                    ) AS pasos,
                    (
                        SELECT GROUP_CONCAT(etiquetas.nombre SEPARATOR ',')
                        FROM etiquetas JOIN etiquetas_receta
                        ON etiquetas.id_etiqueta = etiquetas_receta.id_etiqueta
                        WHERE etiquetas_receta.id_receta = recetas.id_receta
                    ) AS etiquetas
                FROM recetas
                WHERE recetas.id_receta = %s;
            """
            value = (recipe_id,)
            cursor.execute(query, value)
            result = cursor.fetchall()
            return self.format_recipe(result[0])
        finally:
            cursor.close()

    def format_recipe(self, recipe):
        names_list, amounts_list = self.separate_ingredients(recipe[6])
        selected_recipe = {
            'id': recipe[0],
            'nombre': recipe[1],
            'ingredientes': names_list,
            'cantidades': amounts_list,
            'preparacion': recipe[7],
            'tiempo de preparacion': recipe[2],
            'tiempo de coccion': recipe[3],
            'imagen': recipe[4],
            'etiquetas': recipe[8],
            'favorito': recipe[5]
        }
        return selected_recipe
    
    def separate_ingredients(self, ingredients: str):
        names = []
        amounts = []
        ingredient_list = ingredients.split(',')
        for ingredient in ingredient_list:
            name, amount = ingredient.split('(')
            amount = amount.strip(')')
            amounts.append(amount)
            names.append(name.strip())
        return ','.join(names), ','.join(amounts)

    def delete_recipe(self, recipe_id):
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM recetas WHERE id_receta = %s"
            values = (recipe_id,)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()
    
    def update_recipe(self, recipe):
        try:
            cursor = self.connection.cursor()
            query = """UPDATE recetas 
            SET nombre = %s, tiempo_preparacion = %s, tiempo_coccion = %s, imagen = %s, favorito = %s WHERE id_receta = %s"""
            values = (recipe['nombre'], recipe['tiempo de preparacion'], recipe['tiempo de coccion'], recipe['imagen'], recipe['favorito'], recipe['id'])
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

    def check_and_update(self, recipe_details, original):
        delete_ing = self.check_items(original['ingredientes'], recipe_details['ingredientes'])
        delete_prep = self.check_items(original['preparacion'], recipe_details['preparacion'])
        delete_tags = self.check_items(original['etiquetas'], recipe_details['etiquetas'])
        if delete_ing != []:
            for ing in delete_ing:
                self.delete_ingredient_by_name(ing, original['id'])
        for ing in recipe_details['ingredients_id']:
            self.add_recipe_id_to_ingredients(ing, original['id'])
        if delete_prep != []:
            for prep in delete_prep:
                self.delete_method_by_name(prep, original['id'])
        for prep in recipe_details['methods_id']:
            self.add_prep_method_to_recipe(prep, 1, original['id'])
        if delete_tags != []:
            for tag in delete_tags:
                self.delete_tag_by_name(tag, original['id'])
        new_tags = self.check_tags(original['etiquetas'], recipe_details['etiquetas'])
        for tag in new_tags:
            tag_id = self.create_tag(tag)
            self.create_tag_recipe(tag_id, original['id'])

    def check_items(self, original, new):
        original_item = original.split(',')
        new_item = new.split(',')
        for item in new_item:
            if item in original_item:
                original_item.remove(item)
        return original_item
    
    def check_tags(self, original, new):
        original_item = original.split(',')
        new_item = new.split(',')
        for item in new_item:
            if item in original_item:
                new_item.remove(item)
        return new_item

    def delete_ingredient_by_name(self, name, recipe_id):
        try:
            cursor = self.connection.cursor()
            query_get_id = "SELECT id_ingrediente FROM ingredientes WHERE nombre = %s"
            cursor.execute(query_get_id, (name,))
            ingredient_id = cursor.fetchone()

            query = "DELETE FROM ingredientes_receta WHERE id_receta = %s AND id_ingrediente = %s"
            values = (recipe_id, ingredient_id[0])
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()
    
    def delete_tag_by_name(self, name, recipe_id):
        try:
            cursor = self.connection.cursor()
            query_get_id = "SELECT id_etiqueta FROM etiquetas WHERE nombre = %s"
            cursor.execute(query_get_id, (name,))
            tag_id = cursor.fetchone()

            query = "DELETE FROM etiquetas_receta WHERE id_receta = %s AND id_etiqueta = %s"
            values = (recipe_id, tag_id[0])
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

    def delete_method_by_name(self, name, recipe_id):
        try:
            cursor = self.connection.cursor()
            query_get_id = "SELECT id_paso FROM pasos WHERE nombre = %s"
            cursor.execute(query_get_id, (name,))
            prep_id = cursor.fetchone()

            query = "DELETE FROM pasos_receta WHERE id_receta = %s AND id_paso = %s"
            values = (recipe_id, prep_id[0])
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

# TAGS --------------------------------------

    def create_tag(self, tag_name):
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO etiquetas (nombre) VALUES (%s)"
            values = (tag_name,)
            cursor.execute(query, values)
            self.connection.commit()

            cursor.execute("SELECT LAST_INSERT_ID()")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def create_tag_recipe(self, tag_id, recipe_id):
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO etiquetas_receta (id_etiqueta, id_receta) VALUES (%s, %s)"
            values = (tag_id, recipe_id)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()
    
    def search_by_name(self, name):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT recetas.id_receta, recetas.nombre, recetas.tiempo_preparacion, recetas.tiempo_coccion, recetas.creado_el,
                (
                    SELECT GROUP_CONCAT(ingredientes.nombre SEPARATOR ',')
                    FROM ingredientes
                    JOIN ingredientes_receta
                    ON ingredientes.id_ingrediente = ingredientes_receta.id_ingrediente
                    WHERE ingredientes_receta.id_receta = recetas.id_receta
                ) AS ingredientes
                FROM recetas
                WHERE recetas.nombre LIKE %s;
            """
            cursor.execute(query, (f'%{name}%',))

            found_recipes = cursor.fetchall()
            return found_recipes
        finally:
            cursor.close()
            
    def search_by_tags(self, tags):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT recetas.id_receta, recetas.nombre, recetas.tiempo_preparacion, recetas.tiempo_coccion, recetas.creado_el,
            (
                SELECT GROUP_CONCAT(etiquetas.nombre SEPARATOR ', ')
                FROM etiquetas
                JOIN etiquetas_receta
                ON etiquetas.id_etiqueta = etiquetas_receta.id_etiqueta
                WHERE etiquetas_receta.id_receta = recetas.id_receta
            ) AS etiquetas
            FROM recetas
            JOIN etiquetas_receta
            ON recetas.id_receta = etiquetas_receta.id_receta
            JOIN etiquetas
            ON etiquetas_receta.id_etiqueta = etiquetas.id_etiqueta
            WHERE etiquetas.nombre = %s;
            """

            # Ejecutar la consulta SQL pasando las etiquetas como parámetros
            cursor.execute(query, (tags,))
            found_recipes = cursor.fetchall()
            return set(found_recipes)
        finally:
            cursor.close()

    def search_by_prep_time(self, prep_time):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT recetas.id_receta, recetas.nombre, recetas.tiempo_preparacion, recetas.tiempo_coccion, recetas.creado_el,
                (
                    SELECT GROUP_CONCAT(ingredientes.nombre SEPARATOR ',')
                    FROM ingredientes
                    JOIN ingredientes_receta
                    ON ingredientes.id_ingrediente = ingredientes_receta.id_ingrediente
                    WHERE ingredientes_receta.id_receta = recetas.id_receta
                ) AS ingredientes
                FROM recetas
                WHERE recetas.tiempo_preparacion = %s;
            """
            cursor.execute(query, (prep_time,))

            found_recipes = cursor.fetchall()
            return found_recipes
        finally:
            cursor.close()
    
    def search_by_ingredient(self, ingredient):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT recetas.id_receta, recetas.nombre, recetas.tiempo_preparacion, recetas.tiempo_coccion, recetas.creado_el,
                (
                    SELECT GROUP_CONCAT(ingredientes.nombre SEPARATOR ',')
                    FROM ingredientes
                    JOIN ingredientes_receta
                    ON ingredientes.id_ingrediente = ingredientes_receta.id_ingrediente
                    WHERE ingredientes_receta.id_receta = recetas.id_receta
                ) AS ingredientes
                FROM recetas
                JOIN ingredientes_receta
                ON recetas.id_receta = ingredientes_receta.id_receta
                JOIN ingredientes
                ON ingredientes_receta.id_ingrediente = ingredientes.id_ingrediente
                WHERE ingredientes.nombre = %s;
            """
            cursor.execute(query, (ingredient,))

            found_recipes = cursor.fetchall()
            return found_recipes
        finally:
            cursor.close()
# TAG_RECIPE ----------------------------------}

    def select_recipe_of_the_day(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id_receta FROM recetas")
            all_recipes = cursor.fetchall()

            random_recipe = random.choice(all_recipes)
            query_update = "UPDATE recetas SET receta_del_dia = 1, fecha_asignacion = %s WHERE id_receta = %s"
            cursor.execute(query_update, (date.today(), random_recipe[0]))
            self.connection.commit()
        finally:
            cursor.close()
    
    def get_recipe_of_the_day(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
            SELECT r.id_receta, r.nombre, r.tiempo_preparacion, r.tiempo_coccion, r.creado_el,
                   (SELECT GROUP_CONCAT(i.nombre SEPARATOR ', ')
                    FROM ingredientes i
                    JOIN ingredientes_receta ir ON i.id_ingrediente = ir.id_ingrediente
                    WHERE ir.id_receta = r.id_receta
                   ) AS ingredientes
            FROM recetas r
            WHERE receta_del_dia = 1
        """)
            recipe_of_the_day = cursor.fetchone()
            return recipe_of_the_day
        finally:
            cursor.close()

    def reset_recipe_of_the_day(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id_receta FROM recetas WHERE receta_del_dia = 1")
            recipe_of_the_day = cursor.fetchone()

            if recipe_of_the_day:
                query_update = "UPDATE recetas SET receta_del_dia = 0, fecha_asignacion = NULL WHERE id_receta = %s"
                cursor.execute(query_update, (recipe_of_the_day[0],))
        finally:
            cursor.close()

    def has_day_changed(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT fecha_asignacion FROM recetas WHERE receta_del_dia = 1")
            last_assignment_date = cursor.fetchone()

            if last_assignment_date:
                last_assignment_date = last_assignment_date[0]
                current_date = date.today()

                if current_date != last_assignment_date:
                    return True
                else:
                    return False
            else:
                return True

        finally:
            cursor.close()



if __name__ == "__main__":
    db = DBUtils()
    db.connect()
    ing = db.read_ingredients([31, 32, 33])
    print(ing)
    for i in ing:
        for f in i:
            print(f)
# USE recipe_manager;

# -- SELECT * FROM recetas;

# -- SELECT ingredientes

# -- SELECT ingredientes.nombre, ingredientes_receta.cantidad, ingredientes_receta.medida 
# -- FROM ingredientes
# -- JOIN ingredientes_receta
# -- ON ingredientes.id_ingrediente = ingredientes_receta.id_ingrediente
# -- JOIN recetas
# -- ON recetas.id_receta = ingredientes_receta.id_receta
# -- WHERE recetas.id_receta = 3;

# SELECT
#     recetas.id_receta, recetas.nombre, recetas.tiempo_preparacion, 
#     recetas.tiempo_coccion, recetas.imagen, recetas.favorito,
#     (
#         SELECT GROUP_CONCAT(ingredientes.nombre, ' (', ingredientes_receta.cantidad, ' ', ingredientes_receta.medida, ')' SEPARATOR ',')
#         FROM ingredientes JOIN ingredientes_receta
#         ON ingredientes.id_ingrediente = ingredientes_receta.id_ingrediente
#         WHERE ingredientes_receta.id_receta = recetas.id_receta
#     ) AS ingredientes,
#     (
# 		SELECT GROUP_CONCAT(pasos.descripcion SEPARATOR ',')
#         FROM pasos JOIN pasos_receta
#         ON pasos.id_paso = pasos_receta.id_paso
#         WHERE pasos_receta.id_receta = recetas.id_receta
# 	) AS pasos,
#     (
# 		SELECT GROUP_CONCAT(etiquetas.nombre SEPARATOR ',')
#         FROM etiquetas JOIN etiquetas_receta
#         ON etiquetas.id_etiqueta = etiquetas_receta.id_etiqueta
#         WHERE etiquetas_receta.id_receta = recetas.id_receta
#     ) AS etiquetas
# FROM recetas;