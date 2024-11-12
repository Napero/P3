import tkinter as tk
from tkinter import messagebox
import BBSudoku as bb
import sudoku as bt
import copy

# Variables globales para el tablero y el algoritmo seleccionado
tablero = [[0] * 9 for _ in range(9)]
algoritmo_seleccionado = None
grid_entries = [[None for _ in range(9)] for _ in range(9)]  # Matriz para almacenar los widgets Entry
valores_iniciales = set()  # Guardar las posiciones de los valores ingresados manualmente


def reiniciar():
    global tablero, algoritmo_seleccionado, valores_iniciales
    tablero = [[0] * 9 for _ in range(9)]
    algoritmo_seleccionado = None
    valores_iniciales.clear()
    mostrar_pantalla_inicio()


def mostrar_pantalla_inicio():
    limpiar_pantalla()
    lbl = tk.Label(root, text="Seleccione el algoritmo", font=("Arial", 16))
    lbl.grid(row=0, column=0, columnspan=2, pady=20)
    btn_bnb = tk.Button(root, text="B&B", command=lambda: seleccionar_algoritmo("bnb"))
    btn_bt = tk.Button(root, text="Backtracking", command=lambda: seleccionar_algoritmo("bt"))
    btn_bnb.grid(row=1, column=0, pady=10)
    btn_bt.grid(row=1, column=1, pady=10)


def seleccionar_algoritmo(algoritmo):
    global algoritmo_seleccionado
    algoritmo_seleccionado = algoritmo
    mostrar_pantalla_modo_tablero()


def mostrar_pantalla_modo_tablero():
    limpiar_pantalla()
    lbl = tk.Label(root, text="Seleccione el modo de tablero", font=("Arial", 16))
    lbl.grid(row=0, column=0, columnspan=2, pady=20)
    btn_generar = tk.Button(root, text="Generar tablero", command=mostrar_pantalla_dificultad)
    btn_ingresar = tk.Button(root, text="Ingresar manualmente", command=mostrar_pantalla_ingresar)
    btn_generar.grid(row=1, column=0, pady=10)
    btn_ingresar.grid(row=1, column=1, pady=10)
    agregar_boton_reiniciar()


def mostrar_pantalla_dificultad():
    limpiar_pantalla()
    lbl = tk.Label(root, text="Seleccione la dificultad", font=("Arial", 16))
    lbl.grid(row=0, column=0, columnspan=3, pady=20)
    btn_facil = tk.Button(root, text="Fácil", command=lambda: generar_tablero("facil"))
    btn_medio = tk.Button(root, text="Medio", command=lambda: generar_tablero("medio"))
    btn_dificil = tk.Button(root, text="Difícil", command=lambda: generar_tablero("dificil"))
    btn_facil.grid(row=1, column=0, pady=5)
    btn_medio.grid(row=1, column=1, pady=5)
    btn_dificil.grid(row=1, column=2, pady=5)
    agregar_boton_reiniciar()


def generar_tablero(dificultad):
    global tablero, valores_iniciales
    if algoritmo_seleccionado == "bnb":
        tablero = bb.generar_tablero(dificultad)
    elif algoritmo_seleccionado == "bt":
        tablero = bt.generar_tablero(dificultad)
    valores_iniciales = {(i, j) for i in range(9) for j in range(9) if tablero[i][j] != 0}
    mostrar_pantalla_juego()


def mostrar_pantalla_ingresar():
    limpiar_pantalla()
    lbl = tk.Label(root, text="Ingrese el tablero manualmente", font=("Arial", 16))
    lbl.grid(row=0, column=0, columnspan=9, pady=10)
    global tablero
    tablero = [[0] * 9 for _ in range(9)]

    for i in range(9):
        for j in range(9):
            entry = tk.Entry(root, width=2, font=("Arial", 16), justify="center")
            entry.grid(row=i + 1, column=j, padx=5, pady=5)
            grid_entries[i][j] = entry  # Almacena el widget en la matriz para actualizarlo luego

    btn_terminar = tk.Button(root, text="Terminar ingreso", command=validar_y_guardar_tablero_ingresado)
    btn_terminar.grid(row=10, column=0, columnspan=9, pady=10)
    agregar_boton_reiniciar()


def validar_y_guardar_tablero_ingresado():
    global tablero, valores_iniciales
    valores_iniciales.clear()  # Reinicia las posiciones iniciales

    # Cargar los valores del tablero desde los Entry
    for i in range(9):
        for j in range(9):
            val = grid_entries[i][j].get()
            if val.isdigit() and 1 <= int(val) <= 9:
                tablero[i][j] = int(val)
                valores_iniciales.add((i, j))
            elif val == "":
                tablero[i][j] = 0
            else:
                messagebox.showerror("Error de ingreso", "Todos los números deben estar entre 1 y 9.")
                return

    # Verificar si hay duplicados en filas, columnas o cuadrículas 3x3
    if not es_tablero_valido():
        messagebox.showerror("Error", "El tablero ingresado tiene números repetidos en filas, columnas o cuadrículas 3x3.")
        return

    mostrar_pantalla_juego()


def es_tablero_valido():
    # Verificar filas y columnas
    for i in range(9):
        fila_vistos = set()
        columna_vistos = set()
        for j in range(9):
            # Verificación de fila
            if tablero[i][j] != 0:
                if tablero[i][j] in fila_vistos:
                    return False
                fila_vistos.add(tablero[i][j])

            # Verificación de columna
            if tablero[j][i] != 0:
                if tablero[j][i] in columna_vistos:
                    return False
                columna_vistos.add(tablero[j][i])

    # Verificar cuadrículas 3x3
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box_vistos = set()
            for i in range(3):
                for j in range(3):
                    num = tablero[box_row + i][box_col + j]
                    if num != 0:
                        if num in box_vistos:
                            return False
                        box_vistos.add(num)
    return True


def mostrar_pantalla_juego():
    limpiar_pantalla()
    lbl = tk.Label(root, text="Juego de Sudoku", font=("Arial", 16))
    lbl.grid(row=0, column=0, columnspan=9, pady=10)

    for i in range(9):
        for j in range(9):
            val = tablero[i][j]
            entry = tk.Entry(root, width=2, font=("Arial", 16), justify="center", fg="black")
            entry.grid(row=i + 1, column=j, padx=5, pady=5)
            if val != 0:
                entry.insert(0, val)
                entry.config(state="readonly", bg="light grey")  # Cambia a "readonly" después de insertar el valor
            else:
                entry.config(bg="white")  # Deja los espacios vacíos editables con fondo blanco
            grid_entries[i][j] = entry  # Almacena el widget para futuras actualizaciones

    btn_resolver = tk.Button(root, text="Resolver automáticamente", command=resolver_automatico)
    btn_verificar = tk.Button(root, text="Verificar solución", command=verificar_solucion)
    btn_resolver.grid(row=10, column=0, columnspan=4, pady=5)
    btn_verificar.grid(row=10, column=5, columnspan=4, pady=5)
    agregar_boton_reiniciar()


def resolver_automatico():
    global tablero
    tablero_copia = copy.deepcopy(tablero)
    if algoritmo_seleccionado == "bnb":
        if bb.resolver_sudoku(tablero_copia):
            animar_solucion(bb.camino)
    elif algoritmo_seleccionado == "bt":
        if bt.resolver_sudoku(tablero_copia):
            animar_solucion(bt.camino)
    messagebox.showinfo("Resolución completada", "El algoritmo ha terminado de resolver el Sudoku.")


def animar_solucion(camino):
    for paso in camino:
        fila, col, num, _ = paso
        fila -= 1
        col -= 1
        if 0 <= fila < 9 and 0 <= col < 9 and (fila, col) not in valores_iniciales:
            tablero[fila][col] = num
            grid_entries[fila][col].config(state="normal")
            grid_entries[fila][col].delete(0, tk.END)
            grid_entries[fila][col].insert(0, num)
            grid_entries[fila][col].config(state="readonly", fg="blue")
            root.update()
            root.after(200)


def verificar_solucion():
    for i in range(9):
        for j in range(9):
            val = grid_entries[i][j].get()
            if val == "":
                messagebox.showinfo("Verificación", "La solución está incompleta.")
                return
            if val.isdigit() and not es_valido(tablero, i, j, int(val)):
                messagebox.showerror("Verificación", "La solución es incorrecta.")
                return
    messagebox.showinfo("Verificación", "¡La solución es correcta!")


def es_valido(tablero, fila, col, num):
    for i in range(9):
        if tablero[fila][i] == num and i != col:
            return False
        if tablero[i][col] == num and i != fila:
            return False

    inicio_fila = fila - fila % 3
    inicio_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if tablero[i + inicio_fila][j + inicio_col] == num and (i + inicio_fila != fila or j + inicio_col != col):
                return False
    return True


def agregar_boton_reiniciar():
    btn_reiniciar = tk.Button(root, text="Reiniciar", command=reiniciar)
    btn_reiniciar.grid(row=11, column=0, columnspan=9, pady=5)


def limpiar_pantalla():
    for widget in root.winfo_children():
        widget.destroy()


root = tk.Tk()
root.title("Sudoku Solver")
mostrar_pantalla_inicio()
root.mainloop()
