# Resolución de Sudoku

## Descripción General

Este proyecto implementa un programa en Python para resolver tableros de Sudoku utilizando dos enfoques algorítmicos: **Backtracking** y **Branch & Bound (B&B)**. El objetivo es completar un tablero parcialmente lleno de 9x9 siguiendo las reglas del Sudoku, donde cada fila, columna y subcuadro de 3x3 debe contener los números del 1 al 9 sin repeticiones.

La lógica del programa se centra en el archivo `sudoku_logic.py`, que contiene las funciones principales para generar, resolver y validar tableros de Sudoku. La interfaz gráfica es opcional y se incluye en caso de que se quiera visualizar el proceso, pero no afecta el funcionamiento del algoritmo.

## Metodología de Resolución

### Backtracking

El método de **Backtracking** implementado en `sudoku.py` sigue un enfoque de prueba y error para resolver el Sudoku:

1. **Búsqueda de Celdas Vacías**: El algoritmo busca una celda vacía en el tablero.
2. **Colocación de Números**: Intenta colocar números del 1 al 9 en la celda vacía.
3. **Validación**: Cada número es validado según las reglas del Sudoku (no debe repetirse en la misma fila, columna ni subcuadro de 3x3).
4. **Retroceso**: Si un número no es válido, el algoritmo retrocede y prueba con el siguiente número posible.
5. **Terminación**: Este proceso se repite hasta encontrar una solución o hasta que se hayan probado todas las posibilidades.

### Branch & Bound (B&B)

El método de **Branch & Bound** implementado en `B&Bsudoku.py` es una optimización sobre el Backtracking básico. Emplea una heurística para reducir el número de intentos y mejorar la eficiencia:

1. **Heurística de Restricción**: En lugar de seleccionar cualquier celda vacía, el algoritmo prioriza aquellas celdas con menos opciones válidas (es decir, más restringidas). Esto reduce la cantidad de caminos que se deben explorar.
2. **Cálculo de Cotas**: La implementación de B&B incluye "poda" de caminos que no pueden conducir a una solución válida, basándose en las restricciones del Sudoku. Esta poda limita las combinaciones a explorar y acelera el proceso.

## Estructura del Código en `sudoku_logic.py`

El archivo `sudoku_logic.py` contiene las siguientes funciones principales:

- **`es_valido(tablero, fila, col, num)`**: Verifica si colocar un número en una celda específica es válido según las reglas del Sudoku.
- **`encontrar_vacio_menos_candidatos(tablero)`**: Implementa la heurística de Branch & Bound, buscando la celda vacía con el menor número de candidatos posibles.
- **`obtener_candidatos(tablero, fila, col)`**: Retorna una lista de números posibles que pueden colocarse en una celda sin violar las reglas.
- **`resolver_sudoku(tablero)`**: Algoritmo principal que utiliza Backtracking y Branch & Bound para resolver el tablero. Lleva un registro de los nodos explorados y utiliza la poda para optimizar el proceso.
- **`llenar_tablero(tablero)`**: Genera un tablero de Sudoku válido para empezar a resolver.
- **`quitar_numeros(tablero, celdas_a_llenar)`**: Elimina números del tablero para crear un tablero parcial de dificultad específica.
- **`generar_tablero(dificultad)`**: Genera un tablero de Sudoku de acuerdo con el nivel de dificultad (fácil, medio, difícil), configurando el número de celdas llenas inicialmente.

## Análisis de Eficiencia

Para cada enfoque (Backtracking y Branch & Bound), medimos:

1. **Nodos Explorados**: La cantidad de intentos realizados para colocar números válidos antes de resolver el tablero.
2. **Tiempo de Ejecución**: El tiempo necesario para resolver el tablero en función de su dificultad (fácil, medio o difícil).

Estos análisis permiten comparar la eficiencia entre Backtracking puro y la versión optimizada con Branch & Bound.

## Pruebas y Resultados

Realizamos pruebas en tableros de Sudoku de diferentes niveles de dificultad:
- **Fácil**: Entre 35 y 50 números en el tablero inicial.
- **Medio**: Entre 22 y 34 números en el tablero inicial.
- **Difícil**: Entre 10 y 21 números en el tablero inicial.

Los resultados muestran que el uso de Branch & Bound reduce significativamente el número de nodos explorados y el tiempo de ejecución en comparación con Backtracking puro, especialmente en tableros de mayor dificultad.

## Requisitos

- Python 3.8 o superior
- Librerías estándar de Python (`random`, `time`, `tkinter` si se usa la interfaz gráfica)

## Ejecución

Para ejecutar el programa:

1. Si solo deseas ejecutar el algoritmo de resolución, ejecuta el archivo `main.py` sin necesidad de la interfaz gráfica.
2. Para visualizar el proceso de resolución en la interfaz gráfica, asegúrate de tener `sudoku_gui.py` y `sudoku_logic.py` en la misma carpeta y ejecuta `main.py` desde la terminal:

   ```bash
   python main.py
   ```

