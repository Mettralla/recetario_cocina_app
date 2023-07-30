# from db_config import DB_CONFIG
from src.utils.db_config import DB_CONFIG
import mysql.connector
from datetime import date
import random

class DBUtils:
    """A utility class to manage database connections and operations.

    This class provides methods to establish a connection to the database using the provided configuration,
    as well as to disconnect from the database. It also contains methods to perform various database operations.

    Attributes
    ----------
        connection (mysql.connector.connection.MySQLConnection): The database connection object.
    """
    def __init__(self):
        self.connection = None

    def connect(self) -> None:
        """Establishes a connection to the database.

        This method uses the 'DB_CONFIG' dictionary to connect to the database using the 'mysql.connector' library.
        The connection object is stored in the 'connection' attribute of the class.
        """
        self.connection = mysql.connector.connect(**DB_CONFIG, buffered=True)

    def disconnect(self) -> None:
        """Closes the current database connection, if one is active.

        This method closes the database connection represented by the 'connection' attribute of the class.
        """
        if self.connection:
            self.connection.close()

# INGREDIENTS CRUD -------------------------------------------------

    def create_ingredient(self, ingredient_name: str) -> int:
        """Creates a new ingredient in the database or retrieves the ID of an existing ingredient with the given name.

        Parameters
        -----------
            ingredient_name (str): The name of the ingredient to be created or checked.

        Returns
        -------
            int: The ID of the newly created ingredient or the ID of the existing ingredient with the given name.
        """
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
    
    def read_ingredients(self, ingredients_recipe_ids: list[int]) -> list:
        """Retrieves the details of ingredients used in a recipe based on the given list of recipe IDs.

        Parameters
        -----------
            ingredients_recipe_ids (List[int]): A list of recipe IDs to fetch ingredient details.

        Returns
        -------
            List[Tuple(str, float, str)]: A list of tuples, each containing the ingredient name, quantity, and measurement unit.
        """
        cursor = self.connection.cursor()
        ingredients_data = []
        try:
            for id in ingredients_recipe_ids:
                query = f"""SELECT ingredientes.nombre, ingredientes_receta.cantidad, ingredientes_receta.medida 
                        FROM ingredientes JOIN ingredientes_receta
                        ON ingredientes_receta.id_ingrediente = ingredientes.id_ingrediente
                        WHERE ingredientes_receta.id_ingredientes_receta = {id}"""
                cursor.execute(query)
                ingredient = cursor.fetchall()
                ingredients_data.extend(ingredient)
            return ingredients_data
        finally:
            cursor.close()

# INGREDIENTS_RECIPE ---------------------------------

    def add_ingredient_to_recipe(self, ingredient_id: int, amount: int, units: str) -> int:
        """Adds an ingredient to a recipe in the database.

        Parameters
        -----------
            - ingredient_id (int): The ID of the ingredient to be added to the recipe.
            - amount (int): The amount of the ingredient needed in the recipe.
            - units (str): The measurement units for the ingredient (e.g., grams, cups, teaspoons, etc.).

        Returns
        -------
            - int: The ID of the newly created record in the ingredientes_receta table.
        """
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

    def add_recipe_id_to_ingredients(self, ingredient_recipe_id: int, recipe_id: int) -> None:
        """Associates a recipe ID with an existing ingredient record in the ingredientes_receta table.

        This function is used to link an ingredient record to a specific recipe in the database.

        Parameters
        -----------
            - ingredient_recipe_id (int): The ID of the ingredient record (id_ingredientes_receta) to be associated with the recipe.
            - recipe_id (int): The ID of the recipe (id_receta) to which the ingredient should be linked.
        """
        try:
            cursor = self.connection.cursor()
            query = "UPDATE ingredientes_receta SET id_receta = %s WHERE id_ingredientes_receta = %s"
            values = (recipe_id, ingredient_recipe_id)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

    def delete_ingredient_to_recipe(self, ingredient_recipe_id: int) -> None:
        """Deletes an ingredient record from the ingredientes_receta table.
        
        This function is used to remove an ingredient record associated with a recipe from the database.

        Parameters
        -----------
            - ingredient_recipe_id (int): The ID of the ingredient record (id_ingredientes_receta) to be deleted.
        """
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM ingredientes_receta WHERE id_ingredientes_receta = %s"
            values = (ingredient_recipe_id,)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

    def check_record_existence(self, name: str, table: str) -> int:
        """Checks the existence of a record with the given name in the specified table.
        
        This function queries the database table with the provided name and checks if a record exists with the given name.

        Parameters
        -----------
            - name (str): The name to be checked for existence in the table.
            - table (str): The name of the table to search for the record.
        
        Returns
        -------
            - The primary key or unique identifier of the record if it exists, otherwise None.
        """
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {table} WHERE nombre = %s"
        values = (name,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result if result == None else result[0]

# PREP METHODS CRUD -------------------------------------------------

    def create_prep_method(self, prep_method_description: str) -> int:
        """Creates a new preparation method (step) in the database.

        Parameters
        -----------
            - prep_method_description (str): The description of the new preparation method.
        
        Returns
        -------
            - int: The ID of the newly created preparation method (step).
        """
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

    def delete_prep_method(self, prep_method_id: int) -> None:
        """Deletes a preparation method (step) from the database.
        
        This function is used to remove a specific preparation method (step) record from the pasos table.

        Parameters
        -----------
            - prep_method_id (int): The ID of the preparation method (step) record to be deleted.
        """
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM pasos WHERE id_paso = %s"
            values = (prep_method_id,)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

# PREP_METHOD_RECIPE ---------------------------------

    def add_prep_method_to_recipe(self, prep_method_id: int, order: int, recipe_id: int) -> None:
        """Associates a preparation method (step) with a recipe in the database.
        
        This function links a preparation method (step) with a specific recipe and sets the order in which the step should be performed.

        Parameters
        -----------
            - prep_method_id (int): The ID of the preparation method (step) to be associated with the recipe.
            - order (int): The order in which the preparation method (step) should be performed in the recipe.
            - recipe_id (int): The ID of the recipe to which the preparation method (step) should be linked.
        """
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
        """Creates a new recipe in the database.
        
        This function adds a new recipe with the provided details to the recetas table.

        Parameters
        -----------
            - new_recipe (dict): A dictionary containing the details of the new recipe. It should have the following keys:
                - 'name' (str): The name of the recipe.
                - 'prep_time' (int): The preparation time of the recipe in minutes.
                - 'cook_time' (int): The cooking time of the recipe in minutes.
                - 'image' (str): The URL or path of the recipe's image (optional).
                - 'favorite' (bool): Indicates whether the recipe is marked as a favorite (True or False).
        
        Returns
        -------
            - int: The ID of the newly created recipe in the recetas table.
        """
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

    def read_recipes(self) -> list:
        """Retrieves a list of all recipes from the database.
        
        This function fetches information about all recipes stored in the recetas table and also includes a comma-separated list of ingredient names associated with each recipe.

        Parameters
        -----------
            - list: A list of dictionaries, each representing a recipe with the following keys:
                - 'id_receta' (int): The ID of the recipe.
                - 'nombre' (str): The name of the recipe.
                - 'tiempo_preparacion' (int): The preparation time of the recipe in minutes.
                - 'tiempo_coccion' (int): The cooking time of the recipe in minutes.
                - 'creado_el' (str): The timestamp when the recipe was created.
                - 'ingredientes' (str): A comma-separated list of ingredient names used in the recipe.
        """
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
            return cursor.fetchall()        
        finally:
            cursor.close()
    
    def get_edited_data_by_id(self, recipe_id: int) -> list:
        """Retrieves edited data for a specific recipe based on its ID from the database.

        This function fetches information about a specific recipe and the associated ingredients (as a comma-separated list) from the recetas and ingredientes tables in the database.

        Parameters
        ----------
            - recipe_id (int): The ID of the recipe for which edited data is to be retrieved.

        Returns
        -------
            - list: A list of dictionaries, each representing a recipe with the following keys:
                - 'id_receta' (int): The ID of the recipe.
                - 'nombre' (str): The name of the recipe.
                - 'tiempo_preparacion' (int): The preparation time of the recipe in minutes.
                - 'tiempo_coccion' (int): The cooking time of the recipe in minutes.
                - 'creado_el' (str): The timestamp when the recipe was created.
                - 'ingredientes' (str): A comma-separated list of ingredient names used in the recipe.
        """
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
                            recetas WHERE id_receta = %s;"""
            value = (recipe_id,)
            cursor.execute(query, value)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_recipe_by_id(self, recipe_id: int) -> dict:
        """Retrieves a specific recipe and its details from the database based on its ID.

        This function fetches information about a recipe and its associated ingredients, preparation steps, and tags from the database tables recetas, ingredientes, ingredientes_receta, pasos, pasos_receta, etiquetas, and etiquetas_receta.

        Parameters
        ----------
            - recipe_id (int): The ID of the recipe to be retrieved.

        Returns
        -------
            -  dict: A dictionary representing the recipe with the following keys:
                - 'id_receta' (int): The ID of the recipe.
                - 'nombre' (str): The name of the recipe.
                - 'tiempo_preparacion' (int): The preparation time of the recipe in minutes.
                - 'tiempo_coccion' (int): The cooking time of the recipe in minutes.
                - 'imagen' (str): The URL or path of the recipe's image (optional).
                - 'favorito' (bool): Indicates whether the recipe is marked as a favorite (True or False).
                - 'ingredientes' (str): A comma-separated list of ingredient names with their quantity and measurement.
                - 'pasos' (str): A comma-separated list of preparation steps for the recipe.
                - 'etiquetas' (str): A comma-separated list of tags associated with the recipe.
        """
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

    def format_recipe(self, recipe: list):
        """Formats a recipe list to a standardized structure.

        This function takes a recipe list with specific elements and restructures it into a standardized dictionary with more descriptive keys for easier readability and consistency.
        """
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
    
    def separate_ingredients(self, ingredients: str) -> tuple[list[str]]:
        """Separates ingredient names and quantities from a comma-separated string.

        This function takes a comma-separated string of ingredient names with their quantities enclosed in parentheses and separates them into two lists: one containing the ingredient names and another containing the corresponding
        quantities.
        
        Parameters
        ----------
            - ingredients (str): A comma-separated string of ingredient names with their quantities in the format: "ingredient1 (quantity1), ingredient2 (quantity2), ..."
        
        Returns
        -------
        - tuple: A tuple containing two lists:
            - The first list contains the ingredient names.
            - The second list contains the corresponding ingredient quantities.

        Example
        -------
        If ingredients = "Salt (1 tsp), Sugar (2 cups), Flour (500 g)", the function will return: (["Salt", "Sugar", "Flour"], ["1 tsp", "2 cups", "500 g"])
        """
        names = []
        amounts = []
        ingredient_list = ingredients.split(',')
        for ingredient in ingredient_list:
            name, amount = ingredient.split('(')
            amount = amount.strip(')')
            amounts.append(amount)
            names.append(name.strip())
        return ','.join(names), ','.join(amounts)

    def delete_recipe(self, recipe_id: int) -> None:
        """Deletes a recipe and its associated records from the database based on its ID.

        This function deletes a specific recipe and its related records from the database tables recetas, ingredientes_receta, pasos_receta, and etiquetas_receta based on the provided recipe_id.
        
        Parameters
        -------
            - recipe_id (int): The ID of the recipe to be deleted.
        """
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM recetas WHERE id_receta = %s"
            values = (recipe_id,)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()
    
    def update_recipe(self, recipe: dict) -> None:
        """Updates a recipe's information in the database based on the provided data.

        This function updates a recipe's information, including its name, preparation time, cooking time, image URL, and favorite status in the database table recetas. The update is performed based on the recipe's unique ID.

        Parameters
        ----------
            recipe (dict): A dictionary representing the updated recipe with the following keys:
                - 'id' (int): The ID of the recipe to be updated.
                - 'nombre' (str): The updated name of the recipe.
                - 'tiempo de preparacion' (int): The updated preparation time of the recipe in minutes.
                - 'tiempo de coccion' (int): The updated cooking time of the recipe in minutes.
                - 'imagen' (str): The updated URL or path of the recipe's image (optional).
                - 'favorito' (bool): The updated favorite status of the recipe (True or False).
        """
        try:
            cursor = self.connection.cursor()
            query = """UPDATE recetas 
            SET nombre = %s, tiempo_preparacion = %s, tiempo_coccion = %s, imagen = %s, favorito = %s WHERE id_receta = %s"""
            values = (recipe['nombre'], recipe['tiempo de preparacion'], recipe['tiempo de coccion'], recipe['imagen'], recipe['favorito'], recipe['id'])
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

    def check_and_update(self, recipe_details: dict, original: dict) -> None:
        """Checks for changes in the recipe details and performs updates in the database accordingly.

        This function compares the new recipe details (recipe_details) with the original recipe details (original) to identify changes in ingredients, preparation methods, and tags. It then updates the database to reflect the changes.

        Parameters
        ----------
            recipe_details (dict): A dictionary representing the new recipe details with the following keys:
                - 'id' (int): The ID of the recipe being updated.
                - 'ingredientes' (list): A list of ingredient names for the updated recipe.
                - 'preparacion' (list): A list of preparation methods for the updated recipe.
                - 'etiquetas' (list): A list of tags for the updated recipe.
                - 'ingredients_id' (list): A list of ingredient IDs associated with the updated recipe.
                - 'methods_id' (list): A list of preparation method IDs associated with the updated recipe.

            original (dict): A dictionary representing the original recipe details with the following keys:
                - 'id' (int): The ID of the original recipe.
                - 'ingredientes' (list): A list of ingredient names in the original recipe.
                - 'preparacion' (list): A list of preparation methods in the original recipe.
                - 'etiquetas' (list): A list of tags in the original recipe.
        """
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
    
    def check_tags(self, original: str, new: str) -> list[str]:
        """Compares two comma-separated strings and returns items present in the original string but not in the new string.

        This function takes two comma-separated strings, 'original' and 'new', and compares them to identify items present in the 'original' string but not in the 'new' string. The function returns a list containing those items.

        Parameters
        ----------
            original (str): The original comma-separated string.
            new (str): The new comma-separated string.

        Returns
        -------
            list[str]: A list containing items that are present in the 'original' string but not in the 'new' string.

        Example
        -------
            If original = "Salt,Sugar,Flour" and new = "Sugar,Flour", the function will return ['Salt'].
        """
        original_item = original.split(',')
        new_item = new.split(',')
        for item in new_item:
            if item in original_item:
                new_item.remove(item)
        return new_item

    def delete_ingredient_by_name(self, name: str, recipe_id: int):
        """Deletes an ingredient from a recipe by its name and recipe ID.

        This function deletes a specific ingredient from a recipe based on its name and the recipe's unique ID.
        The function first fetches the ingredient ID associated with the given name from the 'ingredientes' table.
        It then deletes the corresponding record from the 'ingredientes_receta' table, which links the ingredient to the recipe.

        Parameters
        ----------
            name (str): The name of the ingredient to be deleted from the recipe.
            recipe_id (int): The ID of the recipe from which the ingredient should be removed.
        """
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

    def delete_tag_by_name(self, name: str, recipe_id: int) -> None:
        """Deletes a tag from a recipe by its name and recipe ID.

        This function deletes a specific tag from a recipe based on its name and the recipe's unique ID.
        The function first fetches the tag ID associated with the given name from the 'etiquetas' table.
        It then deletes the corresponding record from the 'etiquetas_receta' table, which links the tag to the recipe.

        Parameters
        ----------
            name (str): The name of the tag to be deleted from the recipe.
            recipe_id (int): The ID of the recipe from which the tag should be removed.
        """
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

    def delete_method_by_name(self, name: str, recipe_id: int) -> None:
        """Deletes a preparation method from a recipe by its name and recipe ID.

        This function deletes a specific preparation method from a recipe based on its name and the recipe's unique ID.
        The function first fetches the preparation method ID associated with the given name from the 'pasos' table.
        It then deletes the corresponding record from the 'pasos_receta' table, which links the preparation method to the recipe.

        Parameters 
        ----------
            name (str): The name of the preparation method to be deleted from the recipe.
            recipe_id (int): The ID of the recipe from which the preparation method should be removed.
        """
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

    def create_tag(self, tag_name: str) -> int:
        """Creates a new tag in the 'etiquetas' table and returns its ID.

        This function inserts a new tag with the provided name into the 'etiquetas' table. The function returns the ID of the newly created tag.

        Parameters
        ----------
            tag_name (str): The name of the new tag to be created.

        Returns
        -------
            int: The ID of the newly created tag.
        """
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
            
# TAG_RECIPE ------------------------------------

    def create_tag_recipe(self, tag_id: int, recipe_id: int) -> None:
        """Links a tag to a recipe by creating a record in the 'etiquetas_receta' table.

        This function links a tag to a recipe by inserting a new record into the 'etiquetas_receta' table.
        The record establishes a connection between the given tag ID and the given recipe ID.

        Parameters
        ----------
            tag_id (int): The ID of the tag to be linked to the recipe.
            recipe_id (int): The ID of the recipe to which the tag should be linked.
        """
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO etiquetas_receta (id_etiqueta, id_receta) VALUES (%s, %s)"
            values = (tag_id, recipe_id)
            cursor.execute(query, values)
            self.connection.commit()
        finally:
            cursor.close()

# SEARCH ----------------------------------------------------------
    
    def search_by_name(self, name: str) -> list:
        """Searches for recipes with names containing the given search term.

        This function performs a search in the 'recetas' table for recipes with names that contain the provided search term.
        It returns a list of recipes that match the search criteria.

        Parameters
        ----------
            name (str): The search term to look for in recipe names.

        Returns
        -------
            list: A list of recipes matching the search criteria. Each recipe is represented as a tuple with the following elements:
                - ID of the recipe (int).
                - Name of the recipe (str).
                - Preparation time of the recipe in minutes (int).
                - Cooking time of the recipe in minutes (int).
                - Timestamp when the recipe was created (str).
                - Comma-separated string of ingredient names used in the recipe (str).
        """
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

    def search_by_tags(self, tags) -> set:
        """Searches for recipes that have the provided tags.

        This function performs a search in the 'recetas' table for recipes that have the specified tags.
        It returns a set of unique recipes that match the search criteria.

        Parameters
        ----------
            tags (str): The tags to look for in the recipes.

        Returns
        -------
            set: A set of unique recipes matching the search criteria. Each recipe is represented as a tuple with the following elements:
                - ID of the recipe (int).
                - Name of the recipe (str).
                - Preparation time of the recipe in minutes (int).
                - Cooking time of the recipe in minutes (int).
                - Timestamp when the recipe was created (str).
                - Comma-separated string of tags associated with the recipe (str).
        """
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
            cursor.execute(query, (tags,))
            found_recipes = cursor.fetchall()
            return set(found_recipes)
        finally:
            cursor.close()

    def search_by_prep_time(self, prep_time: int) -> list:
        """Searches for recipes with the specified preparation time.

        This function performs a search in the 'recetas' table for recipes that have the specified preparation time.
        It returns a list of recipes that match the search criteria.

        Parameters
        ----------
            prep_time (int): The preparation time of the recipes to search for, measured in minutes.

        Returns
        -------
            list: A list of recipes matching the search criteria. Each recipe is represented as a tuple with the following elements:
                - ID of the recipe (int).
                - Name of the recipe (str).
                - Preparation time of the recipe in minutes (int).
                - Cooking time of the recipe in minutes (int).
                - Timestamp when the recipe was created (str).
                - Comma-separated string of ingredient names used in the recipe (str).
        """
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
    
    def search_by_ingredient(self, ingredient: str) -> list:
        """Searches for recipes that contain the specified ingredient.

        This function performs a search in the 'recetas' table for recipes that contain the provided ingredient.
        It returns a list of recipes that match the search criteria.

        Parameters
        ----------
            ingredient (str): The ingredient to look for in the recipes.

        Returns
        -------
            list: A list of recipes matching the search criteria. Each recipe is represented as a tuple with the following elements:
                - ID of the recipe (int).
                - Name of the recipe (str).
                - Preparation time of the recipe in minutes (int).
                - Cooking time of the recipe in minutes (int).
                - Timestamp when the recipe was created (str).
                - Comma-separated string of ingredient names used in the recipe (str).
        """
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


if __name__ == "__main__":
    db = DBUtils()
    db.connect()
    ing = db.read_ingredients([1,2,4])