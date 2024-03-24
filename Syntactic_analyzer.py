import tkinter as tk
from tkinter import messagebox

class Gramatica:
    def __init__(self, terminales, no_terminales, inicial, producciones):
        self.terminales = terminales
        self.no_terminales = no_terminales
        self.inicial = inicial
        self.producciones = self.parsear_producciones(producciones)

    def parsear_producciones(self, producciones):
        dict_prod = {}
        parts = producciones.split(",")

        for part in parts:
            not_terminal_part, production_part = part.split(";")
            if not_terminal_part not in dict_prod:
                dict_prod[not_terminal_part] = [production_part]
            else:
                dict_prod[not_terminal_part].append(production_part)

        new_dict_prod = {
            key.strip(): [value.strip() for value in values]
            for key, values in dict_prod.items()
        }
        return new_dict_prod

    def generar_cadena(self, palabra):
        return self.derivar(self.inicial, palabra)

    def derivar(self, not_terminal, palabra):
        if not palabra:
            return True

        if not_terminal in self.producciones:
            for produccion in self.producciones[not_terminal]:
                if palabra.startswith(produccion):
                    if self.derivar(produccion, palabra[len(produccion):]):
                        return True

        return False


def verificar_palabra():
    terminales = entrada_terminales.get()
    no_terminales = entrada_no_terminales.get()
    inicial = entrada_inicial.get()
    producciones = entrada_producciones.get()

    gramatica = Gramatica(terminales, no_terminales, inicial, producciones)

    palabra = entrada_palabra.get()
    pertenece = gramatica.generar_cadena(palabra)
    if pertenece:
        messagebox.showinfo("Resultado", f'La palabra "{palabra}" pertenece al lenguaje.')
    else:
        messagebox.showinfo("Resultado", f'La palabra "{palabra}" no pertenece al lenguaje.')

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Verificación de Palabras")

# Crear etiquetas y campos de entrada
tk.Label(ventana, text="Terminales:").grid(row=0, column=0, sticky="w")
entrada_terminales = tk.Entry(ventana)
entrada_terminales.grid(row=0, column=1)

tk.Label(ventana, text="No Terminales:").grid(row=1, column=0, sticky="w")
entrada_no_terminales = tk.Entry(ventana)
entrada_no_terminales.grid(row=1, column=1)

tk.Label(ventana, text="Inicial:").grid(row=2, column=0, sticky="w")
entrada_inicial = tk.Entry(ventana)
entrada_inicial.grid(row=2, column=1)

tk.Label(ventana, text="Producciones:").grid(row=3, column=0, sticky="w")
entrada_producciones = tk.Entry(ventana)
entrada_producciones.grid(row=3, column=1)

tk.Label(ventana, text="Palabra a verificar:").grid(row=4, column=0, sticky="w")
entrada_palabra = tk.Entry(ventana)
entrada_palabra.grid(row=4, column=1)

# Botón para verificar la palabra
boton_verificar = tk.Button(ventana, text="Verificar Palabra", command=verificar_palabra)
boton_verificar.grid(row=5, columnspan=2)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()
