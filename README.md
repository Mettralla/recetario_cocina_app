<p align="center">
 <img src=https://drive.google.com/uc?export=view&id=1gPr8aZ6T70vbZ4W6mSjCt1DXYtrLI26n alt="Banner"></a>
</p>
<h3 align="center">Recetario de Cocina</h3>

---

<p align="center"> Resolucion del Proyecto Integrador Final de la Catedra Programación 1 de la Carrera de Desarrollo de Software de la Universidad Provincial de Administración, Tecnologia y Oficios (UPATECO). Consiste en una aplicacion de escritorio donde puede almacenarse recetas de cocina.
    <br> 
</p>

---

## 📝 Tabla de Contenidos
- [Consigna](#problem_statement)
- [Resolucion](#idea)
- [Instalación/Ejecucion](#getting_started)
- [Vista Previa](#usage)
- [Tecnologias](#tech_stack)
- [Autor](#authors)


## 🧐 Consigna <a name = "problem_statement"></a>

Para este proyecto se deberá diseñar una aplicación de escritorio en la que puedan crear, editar y eliminar recetas.

Todos los incisos que tienen el símbolo '✅' son obligatorios, mientras que aquellos que tienen el símbolo '⭐' son opcionales.

Una receta debe estar compuesta de los siguientes datos:

    - Nombre. ✅
    - Una lista de los ingredientes. ✅
    - Preparación, lista ordenada de pasos a seguir. ✅
    - Imagen/es del plato preparado. Una receta puede o no tener una imagen. ✅
    - Tiempo de preparación (en minutos). ✅
    - Tiempo de cocción (en minutos). ✅
    - Fecha de creación. La fecha y hora en que se creó la receta en la aplicación. ✅
    - Etiquetas: palabras clave. ⭐
    - Es favorita (o no). ⭐

Un ingrediente debe contar con la siguiente información:

    - Nombre. ✅
    - Unidad de medida. ✅
    - Cantidad. ✅

Las funcionalidades que debe tener la aplicación son las siguientes:

    - Crear una receta. ✅
    - Modificar una receta. ✅
    - Eliminar una receta. ✅
    - Mostrar “receta del día” aleatoria en la ventana principal. ⭐
    - Buscar y/o filtrar recetas:
        ¬ Nombre. ⭐
        ¬ Por etiquetas. ⭐
        ¬ Tiempo de preparación. ⭐
        ¬ Ingredientes. ⭐

Debe contar con las siguientes vistas:

    - Recetario. Ventana principal por defecto.
    - Se muestra un listado de todas las recetas. ✅
    - Se mostrará como primera receta de lista a la “receta del día”, la cual debe tener un formato distinto a las demás recetas. ⭐
    - Muestra una receta ya existente. ✅
    - Carga/modificación de una receta. ✅
    - Búsqueda y filtro. La ventana deberá tener un campo de búsqueda, por nombre y/o etiqueta. Una vez filtrados las recetas, se las mostrará en una lista.⭐


## 💡 Resolucion <a name = "idea"></a>


Estructura del proyecto:

    .
    ├── csv_files                       # Ficheros csv
    │   ├── ingredients_temp.csv            # Lista temporal de ingredientes
    │   ├── method_list_temp.csv            # Lista temporal de pasos
    │   ├── recipe_of_the_day.csv           # Registro de la receta del dia
    │   └── recipes.csv                     # Lista de recetas
    ├── images                          # Imagenes usadas en el proyecto
    │   ├── get_destination.py              # Detecta ruta relativa del fichero
    │   ├── empty_star.png                  # Iconos de favorito
    │   └── star.png                        # Iconos de favorito
    ├── modules                         # Modulos/Clases Auxiliares
    │   ├── AddIngredient.py                # Ventana que agrega ingrediente
    │   ├── AddMethod.py                    # Ventana que agrega paso
    │   ├── EditRecipe.py                   # Ventana editar receta
    │   ├── NewRecipe.py                    # Ventana crear receta
    │   ├── ReadRecipe.py                   # Ventana leer receta
    │   ├── Ingredient.py                   # Objeto Ingrediente
    │   ├── Recipe.py                       # Objeto Receta
    │   └── globalVar.py                    # Lista de Variables Constantes
    ├── .gitignore                            
    ├── main.py                         # Ventana principal
    └── README.md

## 🏁 Instalación/Ejecución <a name = "getting_started"></a>

Clonar el repositorio

```bash
git clone git@github.com:Mettralla/recetario_cocina_app.git
```

Ir al directorio del proyecto

```bash
cd recetario_cocina_app
```

Iniciar programa

```bash
python main.py
```

## 🎈 Vista Previa <a name="usage"></a>


- Ventana Principal

![App Screenshot](https://drive.google.com/uc?export=view&id=1EQMfyEnTBAVv_2S9p819i3daVu2uNfUT)
<br>

- Ventana Agregar Receta
<br>

![App Screenshot](https://drive.google.com/uc?export=view&id=1lPLi8Iu2l4V33RcDV900WpURVBbzx3JS)

- Ventana Editar Receta
<br>

![App Screenshot](https://drive.google.com/uc?export=view&id=1HeO9ecogyfXjUoVZsd8tpEZt8MGsmBGE)

- Ventana Ver Receta
<br>

![App Screenshot](https://drive.google.com/uc?export=view&id=1BkQi30wDJ-kj1drPEkVBkZl206x4LflN)

## ⛏️ Tecnologias <a name = "tech_stack"></a>

- [Python 3.10.0](https://www.python.org) - Lenguaje
- Librerias usadas:
    - [Tkinter](https://docs.python.org/es/3/library/tkinter.html) - Interface de Python para Tcl/Tk
    - [csv](https://docs.python.org/3/library/csv.html) - Lectura y Escritura de Archivos CSV
    - [datetime](https://docs.python.org/es/3/library/datetime.html) - Tipos básicos de fecha y hora
    - [os](https://docs.python.org/es/3/library/datetime.html) - Interfaces misceláneas del sistema operativo
    - [random](https://docs.python.org/es/3.10/library/random.html?highlight=random#module-random) - Generar números pseudoaleatorios
    - [PIL](https://github.com/python-pillow/Pillow/) - Python Imaging Library

## ✍️ Autor <a name = "authors"></a>
- Daniel Tejerina ([@mettralla](https://github.com/mettralla)) - [Linkedin](https://www.linkedin.com/in/daniel-alejandro-tejerina/)