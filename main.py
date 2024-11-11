import tkinter as tk
from tkinter import messagebox
import BBSudoku as bb
import sudoku as bt
import copy

# Variables globales para el tablero y el algoritmo seleccionado
tablero = [[0] * 9 for _ in range(9)]
algoritmo_seleccionado = None
grid_entries = [[None for _ in range(9)] for _ in range(9)]  # Matriz para almacenar los widgets Entry


def reiniciar():
    global tablero, algoritmo_seleccionado
    tablero = [[0] * 9 for _ in range(9)]
    algoritmo_seleccionado = None
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


def generar_tablero(dificultad):
    global tablero
    if algoritmo_seleccionado == "bnb":
        tablero = bb.generar_tablero(dificultad)
    elif algoritmo_seleccionado == "bt":
        tablero = bt.generar_tablero(dificultad)
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

    btn_terminar = tk.Button(root, text="Terminar ingreso", command=guardar_tablero_ingresado)
    btn_terminar.grid(row=10, column=0, columnspan=9, pady=10)


def guardar_tablero_ingresado():
    global tablero
    for i in range(9):
        for j in range(9):
            val = grid_entries[i][j].get()
            tablero[i][j] = int(val) if val.isdigit() else 0
    mostrar_pantalla_juego()


def mostrar_pantalla_juego():
    limpiar_pantalla()
    lbl = tk.Label(root, text="Juego de Sudoku", font=("Arial", 16))
    lbl.grid(row=0, column=0, columnspan=9, pady=10)

    for i in range(9):
        for j in range(9):
            val = tablero[i][j]
            entry = tk.Entry(root, width=2, font=("Arial", 16), justify="center",
                             state="disabled" if val != 0 else "normal",
                             fg="black", bg="light grey" if val != 0 else "white")
            entry.insert(0, val if val != 0 else "")
            entry.grid(row=i + 1, column=j, padx=5, pady=5)
            grid_entries[i][j] = entry  # Almacena el widget para futuras actualizaciones

    btn_resolver = tk.Button(root, text="Resolver automáticamente", command=resolver_automatico)
    btn_verificar = tk.Button(root, text="Verificar solución", command=verificar_solucion)
    btn_resolver.grid(row=10, column=0, columnspan=4, pady=5)
    btn_verificar.grid(row=10, column=5, columnspan=4, pady=5)


def resolver_automatico():
    global tablero
    tablero_copia = copy.deepcopy(tablero)
    if algoritmo_seleccionado == "bnb":
        if bb.resolver_sudoku(tablero_copia):
            animar_solucion(bb.camino)
    elif algoritmo_seleccionado == "bt":
        if bt.resolver_sudoku(tablero_copia):
            animar_solucion(bt.camino)


def animar_solucion(camino):
    for paso in camino:
        fila, col, num, _ = paso
        fila -= 1
        col -= 1
        if 0 <= fila < 9 and 0 <= col < 9:
            tablero[fila][col] = num
            grid_entries[fila][col].config(state="normal")
            grid_entries[fila][col].delete(0, tk.END)
            grid_entries[fila][col].insert(0, num)
            grid_entries[fila][col].config(state="disabled", fg="blue")
            root.update()
            root.after(200)


def actualizar_pantalla_juego():
    for i in range(9):
        for j in range(9):
            val = tablero[i][j]
            entry = grid_entries[i][j]
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, val if val != 0 else "")
            entry.config(state="disabled" if val != 0 else "normal",
                         fg="black", bg="light grey" if val != 0 else "white")


def verificar_solucion():
    if algoritmo_seleccionado == "bnb":
        if bb.resolver_sudoku(tablero):
            messagebox.showinfo("Verificación", "¡La solución es correcta!")
        else:
            messagebox.showerror("Verificación", "La solución es incorrecta.")
    elif algoritmo_seleccionado == "bt":
        if bt.resolver_sudoku(tablero):
            messagebox.showinfo("Verificación", "¡La solución es correcta!")
        else:
            messagebox.showerror("Verificación", "La solución es incorrecta.")


def limpiar_pantalla():
    for widget in root.winfo_children():
        widget.destroy()


root = tk.Tk()
root.title("Sudoku Solver")
mostrar_pantalla_inicio()
root.mainloop()
