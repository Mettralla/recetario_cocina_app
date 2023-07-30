"""Setup Script for Recipe Manager Database Tables

This script creates the necessary tables for the Recipe Manager application using the configuration from 'db_config.py'.
It connects to the MySQL database server using the credentials specified in 'DB_CONFIG' and creates the following tables:
- 'recetas': Contains information about recipes.
- 'ingredientes': Contains information about ingredients.
- 'ingredientes_receta': Establishes a many-to-many relationship between recipes and ingredients.
- 'pasos': Contains information about preparation steps for recipes.
- 'pasos_receta': Establishes a many-to-many relationship between recipes and preparation steps.
- 'etiquetas': Contains information about tags for categorizing recipes.
- 'etiquetas_receta': Establishes a many-to-many relationship between recipes and tags.

Note: Before running this script, ensure that the 'db_config.py' file contains the correct database connection configuration.

Usage:
    - Run this script to create the necessary tables in the database.
    - Ensure that the 'DB_CONFIG' dictionary in 'db_config.py' contains the appropriate connection details.
"""

from db_config import DB_CONFIG
import mysql.connector

# Establish a connection to the database
conn = mysql.connector.connect(user= DB_CONFIG['user'], password= DB_CONFIG['password'], host= DB_CONFIG['host'])
cur = conn.cursor()

# Define table creation queries
cur.execute("CREATE DATABASE IF NOT EXISTS recipe_manager")
cur.execute("USE recipe_manager")

recipes = """CREATE table IF NOT EXISTS recetas(
                    id_receta INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                    nombre VARCHAR(75) NOT NULL,
                    tiempo_preparacion INT NOT NULL,
                    tiempo_coccion INT NOT NULL,
                    creado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                    imagen VARCHAR(75) DEFAULT NULL,
                    favorito BOOLEAN)"""

ingredients = """CREATE table IF NOT EXISTS ingredientes (
                        id_ingrediente INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                        nombre VARCHAR(75) NOT NULL)"""

ingredients_recipe = """CREATE table IF NOT EXISTS ingredientes_receta (
                        id_ingredientes_receta INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                        id_ingrediente INT NOT NULL,
                        id_receta INT,
                        cantidad SMALLINT NOT NULL,
                        medida VARCHAR(25) NOT NULL,
                        FOREIGN KEY (id_receta) REFERENCES recetas (id_receta) ON DELETE CASCADE,
                        FOREIGN KEY (id_ingrediente) REFERENCES ingredientes (id_ingrediente) ON DELETE CASCADE)"""

prep_steps = """CREATE table IF NOT EXISTS pasos (
                        id_paso INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                        descripcion VARCHAR(255))"""

prep_steps_recipe = """CREATE table IF NOT EXISTS pasos_receta (
                        id_pasos_receta INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                        id_paso INT NOT NULL,
                        id_receta INT,
                        orden TINYINT NOT NULL,
                        FOREIGN KEY (id_receta) REFERENCES recetas (id_receta) ON DELETE CASCADE,
                        FOREIGN KEY (id_paso) REFERENCES pasos (id_paso) ON DELETE CASCADE)"""

tags = """CREATE table IF NOT EXISTS etiquetas (
                id_etiqueta INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                nombre VARCHAR(45))"""

tags_recipe = """CREATE table IF NOT EXISTS etiquetas_receta (
                id_etiquetas_receta INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                id_etiqueta INT NOT NULL,
                id_receta INT NOT NULL,
                FOREIGN KEY (id_receta) REFERENCES recetas (id_receta) ON DELETE CASCADE,
                FOREIGN KEY (id_etiqueta) REFERENCES etiquetas (id_etiqueta) ON DELETE CASCADE)"""

# Execute table creation queries
cur.execute(recipes)
cur.execute(ingredients)
cur.execute(prep_steps)
cur.execute(tags)
cur.execute(ingredients_recipe)
cur.execute(prep_steps_recipe)
cur.execute(tags_recipe)

# Commit the changes and close the connection
conn.commit()
conn.close()
