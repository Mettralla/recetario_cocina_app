import mysql.connector
from db_config import DB_CONFIG

def seed_data():
    conn = mysql.connector.connect(user=DB_CONFIG['user'], password=DB_CONFIG['password'], host=DB_CONFIG['host'], database='recipe_manager')
    cur = conn.cursor()

    # Insertar ingredientes
    ingredients_data = [
        ('Sal',),
        ('Pimienta',),
        ('Ajo',),
        ('Cebolla',),
        ('Aceite de oliva',),
        ('Tomate',),
        ('Papa',),
        ('Zanahoria',),
        ('Pollo',),
        ('Arroz',),
    ]
    cur.executemany("INSERT INTO ingredientes (nombre) VALUES (%s)", ingredients_data)

    # Insertar recetas
    recipes_data = [
        ('Pollo al horno', 30, 60, True),
        ('Ensalada de tomate', 15, 0, False),
        ('Arroz con pollo', 20, 40, False),
        ('Sopa de cebolla', 10, 30, False),
        ('Papas fritas', 5, 20, True),
        ('Zanahorias al vapor', 10, 15, False),
        ('Pollo a la parrilla', 25, 30, False),
        ('Arroz con verduras', 15, 25, False),
        ('Tortilla de patatas', 15, 25, True),
        ('Ensalada de pollo', 20, 0, False),
    ]
    cur.executemany("INSERT INTO recetas (nombre, tiempo_preparacion, tiempo_coccion, favorito) VALUES (%s, %s, %s, %s)", recipes_data)

    # Insertar ingredientes en recetas
    ingredient_recipe_data = [
        (1, 1, 1, 'pizca'),
        (1, 2, 1, 'pizca'),
        (2, 6, 1, 'unidad'),
        (3, 9, 1, 'diente'),
        (4, 3, 2, 'unidad'),
        (5, 7, 2, 'cucharada'),
        (6, 8, 2, 'unidad'),
        (7, 10, 2, 'unidad'),
        (8, 5, 3, 'cucharada'),
        (9, 4, 3, 'pieza'),
    ]
    cur.executemany("INSERT INTO ingredientes_receta (id_ingrediente, id_receta, cantidad, medida) VALUES (%s, %s, %s, %s)", ingredient_recipe_data)

    # Insertar pasos en recetas
    steps_data = [
        ('Precalienta el horno a 180°C.',),
        ('Sazona el pollo con sal y pimienta.',),
        ('Coloca el pollo en una bandeja para hornear.',),
        ('Hornea el pollo durante 60 minutos.',),
        ('Sirve caliente y disfruta.',),
        ('Lava y corta los tomates en rodajas.',),
        ('Coloca las rodajas de tomate en un plato.',),
        ('Agrega un poco de aceite de oliva y sal al gusto.',),
        ('Decora con hojas de albahaca fresca.',),
    ]
    cur.executemany("INSERT INTO pasos (descripcion) VALUES (%s)", steps_data)

    recipe_steps_data = [
        (1, 1, 1),
        (1, 2, 2),
        (1, 3, 3),
        (1, 4, 4),
        (2, 5, 1),
        (2, 6, 2),
        (2, 7, 3),
        (2, 8, 4),
    ]
    cur.executemany("INSERT INTO pasos_receta (id_paso, id_receta, orden) VALUES (%s, %s, %s)", recipe_steps_data)

    # Insertar etiquetas
    tags_data = [
        ('Fácil',),
        ('Rápido',),
        ('Saludable',),
        ('Vegetariano',),
        ('Sin gluten',),
        ('Verano',),
        ('Invierno',),
        ('Económico',),
    ]
    cur.executemany("INSERT INTO etiquetas (nombre) VALUES (%s)", tags_data)

    # Insertar etiquetas en recetas
    recipe_tags_data = [
        (1, 1),
        (2, 1),
        (2, 2),
        (3, 2),
        (3, 3),
        (4, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 6),
        (8, 7),
        (9, 8),
        (9, 9),
        (10, 10),
    ]
    cur.executemany("INSERT INTO etiquetas_receta (id_etiqueta, id_receta) VALUES (%s, %s)", recipe_tags_data)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    seed_data()
