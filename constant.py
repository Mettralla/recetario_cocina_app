import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas a carpetas y archivos

# Carpeta de imágenes
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

# Carpeta de archivos fuente
SRC_DIR = os.path.join(BASE_DIR, 'src')

# Archivo de la clase Ingrediente
INGREDIENT_FILE = os.path.join(SRC_DIR, 'Ingredient.py')

# Archivo de la clase Receta
RECIPE_FILE = os.path.join(SRC_DIR, 'Recipe.py')

# Carpeta de ventanas de la aplicación
WINDOWS_DIR = os.path.join(SRC_DIR, 'windows')

# Archivo de la ventana para agregar ingredientes
ADD_INGREDIENT_FILE = os.path.join(WINDOWS_DIR, 'AddIngredient.py')

# Archivo de la ventana para agregar pasos
ADD_METHOD_FILE = os.path.join(WINDOWS_DIR, 'AddMethod.py')

# Archivo de la ventana para editar recetas
EDIT_RECIPE_FILE = os.path.join(WINDOWS_DIR, 'EditRecipe.py')

# Archivo de la ventana para crear nuevas recetas
NEW_RECIPE_FILE = os.path.join(WINDOWS_DIR, 'NewRecipe.py')

# Archivo de la ventana para leer recetas
READ_RECIPE_FILE = os.path.join(WINDOWS_DIR, 'ReadRecipe.py')

# Carpeta de utilidades auxiliares
UTILS_DIR = os.path.join(SRC_DIR, 'utils')

# Archivo de configuración de la base de datos
DB_CONFIG_FILE = os.path.join(UTILS_DIR, 'db_config.py')

# Archivo con utilidades para interactuar con la base de datos
DB_UTILS_FILE = os.path.join(UTILS_DIR, 'db_utils.py')

# Archivo principal de la aplicación
# MAIN_FILE = os.path.join(BASE_DIR, 'main.py')
