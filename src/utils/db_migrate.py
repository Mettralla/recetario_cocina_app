from db_config import DB_CONFIG
import mysql.connector

conn = mysql.connector.connect(user= DB_CONFIG['user'], password= DB_CONFIG['password'], host= DB_CONFIG['host'])
cur = conn.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS recipe_manager")
cur.execute("USE recipe_manager")

recipes = """CREATE table IF NOT EXISTS recetas(
                    id_receta INT NOT NULL AUTO_INCREMENT UNIQUE PRIMARY KEY,
                    nombre VARCHAR(75) NOT NULL,
                    tiempo_preparacion INT NOT NULL,
                    tiempo_coccion INT NOT NULL,
                    creado_el TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                    imagen VARCHAR(75) DEFAULT NULL,
                    favorito BOOLEAN,
                    receta_del_dia BOOLEAN DEFAULT 0,
                    fecha_asignacion DATE DEFAULT NULL)"""

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

cur.execute(recipes)
cur.execute(ingredients)
cur.execute(prep_steps)
cur.execute(tags)
cur.execute(ingredients_recipe)
cur.execute(prep_steps_recipe)
cur.execute(tags_recipe)

conn.commit()
conn.close()

