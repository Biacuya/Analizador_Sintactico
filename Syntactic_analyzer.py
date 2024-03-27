import tkinter as tk
from tkinter import Toplevel, Label
from tkinter import messagebox
from graphviz import Digraph
from tree_graph import Graphic_tree as gt
import subprocess


class Gramatica:
    # Creación del constructor de la clase gramatica
    def __init__(self, terminales, no_terminales, inicial, producciones):
        self.terminales = terminales
        self.no_terminales = no_terminales
        self.inicial = inicial
        # Se manejan dos diccionarios de producciones por practicidad
        self.producciones = self.parsear_producciones(producciones)
        self.producciones_two = self.parsear_producciones_two(producciones)

    # Método encargado de convertir las producciones en un diccionario
    def parsear_producciones(self, producciones):
        dict_prod = {}
        parts = producciones.split(",")  # Se separan las particiones por ","
        count = 0

        for part in parts:
            not_terminal_part, production_part = part.split(
                ";"
            )  # Aprovechando el formato de las producciones las separamos, quedando la parte no terminal y la producción aparte
            if not_terminal_part not in dict_prod:
                dict_prod[not_terminal_part] = [production_part]

            else:
                count += 1
                dict_prod[not_terminal_part + str(count)] = [
                    production_part
                ]  # Si la parte terminal de la producción ya esta agregada (en este caso sería la key del diccionario) le agreamos un sufijo númerico para hacer que not_terminal_part sea unica.

        return dict_prod

    # Segundo método de parsear las producciones
    def parsear_producciones_two(self, producciones):
        dict_prod = {}
        parts = producciones.split(",")

        for part in parts:
            not_terminal_part, production_part = part.split(";")
            if not_terminal_part not in dict_prod:
                dict_prod[not_terminal_part] = [production_part]
            else:
                dict_prod[not_terminal_part].append(
                    production_part
                )  # Aquí en vez de agregar un sufijo agregamos una lista de producciones a not_terminak_part en caso de que el simbolo terminal sea el mismo para todas las prdoucciones

        # Le damos un nuevo formato al diccionario
        new_dict_prod = {
            key.strip(): [value.strip() for value in values]
            for key, values in dict_prod.items()
        }
        return new_dict_prod

    # Método para graficar el arbol de deriviación general de la gramatica
    def graph_tree(self):

        dict_result = {}
        count = {}

        # Damos formato al diccionario
        for key, values in self.producciones.items():
            separate_values = [[caracter for caracter in value] for value in values]
            dict_result[key.strip()] = [
                item for sublist in separate_values for item in sublist
            ]
        # Se proede a dejar cada valor de la producción como unico
        for key, values in dict_result.items():
            dict_result[key.strip()] = []
            for value in values:
                # Si el valor ya está presente en count, incrementamos el contador y agregamos el sufijo numérico
                if value in count:
                    count[value] += 1
                    new_value = f"{value}{count[value]}"
                    dict_result[key.strip()].append(new_value)
                # Si es un valor único, lo agregamos tal cual
                else:
                    count[value] = 0
                    dict_result[key.strip()].append(value)

        # Convetirmos el diccionario en una lista de tuplas
        list_tuples = list(dict_result.items())
        # Pasamos nuestra lista de tuplas al método drwa_tree para graficar
        gt.draw_tree(list_tuples)

    def generar_cadena(self, palabra):
        return self.derivar(self.inicial, palabra)

    # Método encargado de verificar si una palabra pertecene o no a una gramatica
    def derivar(self, not_terminal, palabra):
        count = 0

        # Si la palabra queda vacia significa que pertenece y retornamos true
        if not palabra:
            return True
        # Nos aseguramos que nuestra parte no terminal este en nuestro diccionario de producciones
        if not_terminal in self.producciones_two:

            for produccion in self.producciones_two[not_terminal]:
                count += 1

                # Hacemos que cada parte no terminal sea unica
                identifier = not_terminal + str(count)

                # Verificamos si la palabra pertenece a la gramatica
                if palabra.startswith(produccion[0]):
                    gt.create_graphic_horinzontal(
                        gt, identifier, f"Nodo: {not_terminal}", identifier, palabra
                    )
                    # Vamos eliminando los caracteres de la palabra procesada
                    if self.derivar(produccion[1:], palabra[1:]):
                        # print("if final")
                        return True

        return False


# Método encargado de llamar los anteriores métodos y pasar datos a la interfaz
def verificar_palabra():
    terminales = entrada_terminales.get()
    no_terminales = entrada_no_terminales.get()
    inicial = entrada_inicial.get()
    producciones = entrada_producciones.get()
    list_of_word = []

    gramatica = Gramatica(terminales, no_terminales, inicial, producciones)
    # gramatica = Gramatica("a, b", "S, A", "S", "S;aA, A;aA, A;bA, A;b")
    palabra = entrada_palabra.get()
    list_of_word.append(palabra)
    # palabras = ["aabb"]

    for palabra in list_of_word:
        pertenece = gramatica.generar_cadena(palabra)
        if pertenece:
            messagebox.showinfo(
                "Resultado", f'La palabra "{palabra}" pertenece al lenguaje.'
            )
            gramatica.graph_tree()
            list_of_word = []
        else:
            messagebox.showinfo(
                "Resultado", f'La palabra "{palabra}" no pertenece al lenguaje.'
            )
            boton_arbolH.config(state="disabled")
            boton_arbolV.config(state="disabled")
            list_of_word = []


def mostrar_grafico():
    terminales = entrada_terminales.get()
    no_terminales = entrada_no_terminales.get()
    inicial = entrada_inicial.get()
    producciones = entrada_producciones.get()

    gramatica = Gramatica(terminales, no_terminales, inicial, producciones)
    gramatica.graph_tree()

    # Crear una nueva ventana para mostrar el gráfico
    ventana_grafico = Toplevel(ventana)
    ventana_grafico.title("Gráfico de Árbol")

    # Obtener el tamaño de la imagen del gráfico
    imagen_grafico = tk.PhotoImage(file="arbol_horizontal.png")
    ancho = imagen_grafico.width()
    alto = imagen_grafico.height()

    # Ajustar el tamaño de la ventana al tamaño de la imagen
    ventana_grafico.geometry(f"{ancho}x{alto}")

    # Crear un lienzo del mismo tamaño que la imagen
    lienzo_grafico = tk.Canvas(ventana_grafico, width=ancho, height=alto)
    lienzo_grafico.pack()

    # Mostrar la imagen en el lienzo
    lienzo_grafico.create_image(0, 0, anchor="nw", image=imagen_grafico)

    ventana_grafico.mainloop()


def abrir_arbol_vertical():
    ruta_archivo = "Digraph.gv.pdf"
    try:
        subprocess.Popen(["xdg-open", ruta_archivo])  # Para Linux
    except FileNotFoundError:
        try:
            subprocess.Popen(["open", ruta_archivo])  # Para macOS
        except FileNotFoundError:
            subprocess.Popen(["start", "", ruta_archivo], shell=True)  # Para Windows


# Luego puedes llamar a esta función pasando la ruta del archivo PDF que quieres abrir


# if __name__ == "__main__":
#     verificar_palabra()

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("450x250")
ventana.title("Verificación de Palabras")
ventana.configure(bg="lightblue")

# Crear etiquetas y campos de entrada

tk.Label(ventana, bg="lightblue", text="Terminales:").grid(row=0, column=0, sticky="w")
entrada_terminales = tk.Entry(ventana)
entrada_terminales.grid(row=0, column=2)

tk.Label(ventana, bg="lightblue", text="No Terminales:").grid(
    row=1, column=0, sticky="w"
)
entrada_no_terminales = tk.Entry(ventana)
entrada_no_terminales.grid(row=1, column=2)

tk.Label(ventana, bg="lightblue", text="Inicial:").grid(row=2, column=0, sticky="w")
entrada_inicial = tk.Entry(ventana)
entrada_inicial.grid(row=2, column=2)

tk.Label(ventana, bg="lightblue", text="Producciones:").grid(
    row=3, column=0, sticky="w"
)
entrada_producciones = tk.Entry(ventana)
entrada_producciones.grid(row=3, column=2)

tk.Label(ventana, bg="lightblue", text="Palabra a verificar:").grid(
    row=4, column=0, sticky="w"
)
entrada_palabra = tk.Entry(ventana)
entrada_palabra.grid(row=4, column=2)

tk.Label(ventana, bg="lightblue").grid(row=5)

tk.Label(
    ventana,
    bg="lightblue",
    text=" Insertar como mínimo dos símbolos \nterminales, tres no terminales y \ntres producciones",
).grid(row=9, column=1, sticky="w")
tk.Label(ventana, bg="lightblue", text="Warning: ", fg="brown", font=("bold")).grid(
    row=9
)
tk.Label(ventana, bg="lightblue").grid(row=10)

# Botón para verificar la palabra
boton_verificar = tk.Button(
    ventana, text="Verificar Palabra", command=verificar_palabra, bg="#0080FF"
)
boton_verificar.grid(row=8, columnspan=1)
boton_arbolH = tk.Button(
    ventana, text="arbol Horizontal", command=mostrar_grafico, bg="#0080FF"
)
boton_arbolH.grid(row=8, columnspan=2)


boton_arbolV = tk.Button(
    ventana, text="arbol vertical", command=abrir_arbol_vertical, bg="#0080FF"
)
boton_arbolV.grid(row=8, columnspan=3)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()
