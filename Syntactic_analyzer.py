import tkinter as tk
from tkinter import messagebox
from graphviz import Digraph
from tree_graph import Graphic_tree as gt


class Gramatica:
    def __init__(self, terminales, no_terminales, inicial, producciones):
        self.terminales = terminales
        self.no_terminales = no_terminales
        self.inicial = inicial
        self.producciones = self.parsear_producciones(producciones)
        self.producciones_two = self.parsear_producciones_two(producciones)

    def parsear_producciones(self, producciones):
        dict_prod = {}
        parts = producciones.split(",")
        count = 0

        for part in parts:
            not_terminal_part, production_part = part.split(";")
            if not_terminal_part not in dict_prod:
                dict_prod[not_terminal_part] = [production_part]

            else:
                count += 1
                dict_prod[not_terminal_part + str(count)] = [production_part]

        return dict_prod

    def parsear_producciones_two(self, producciones):
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

    def process_string(self, list_values: list):
        count = {}
        result = []
        for char in list_values:
            if char not in count:
                count[char] = 0
                result.append(char)
            else:
                count[char] += 1
                result.append(char + str(count[char] + 1))

        return result

    def draw_tree(self, tree_data):
        dot = Digraph(comment="Tree")
        nodes = set()
        for parent, children in tree_data:
            nodes.add(parent)
            for child in children:
                nodes.add(child)
                dot.edge(parent, child)
        for node in nodes:
            dot.node(node)
        return dot

    def graph_tree(self):

        dict_result = {}
        count = {}

        for key, values in self.producciones.items():
            separate_values = [[caracter for caracter in value] for value in values]
            dict_result[key.strip()] = [
                item for sublist in separate_values for item in sublist
            ]

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

        list_tuples = list(dict_result.items())
        self.draw_tree(list_tuples).view()
        print(dict_result)
        print(list_tuples)

    def generar_cadena(self, palabra):
        return self.derivar(self.inicial, palabra)

    def derivar(self, not_terminal, palabra):
        count = 0

        if not palabra:
            print(f"palabra: {palabra}")
            return True

        if not_terminal in self.producciones_two:

            for produccion in self.producciones_two[not_terminal]:
                count += 1

                identifier = not_terminal + str(count)
                if identifier == not_terminal:
                    count += 1
                    print("identificador duplicado")
                print("Identificador: " + identifier)

                if palabra.startswith(produccion[0]):
                    count += 1
                    gt.create_graphic_horinzontal(
                        gt, identifier, f"Nodo: {not_terminal}", identifier, palabra
                    )

                    if self.derivar(produccion[1:], palabra[1:]):
                        # print("if final")
                        return True

        return False


def verificar_palabra():
    terminales = entrada_terminales.get()
    no_terminales = entrada_no_terminales.get()
    inicial = entrada_inicial.get()
    producciones = entrada_producciones.get()

    gramatica = Gramatica(terminales, no_terminales, inicial, producciones)
    # gramatica = Gramatica("a, b", "S, A", "S", "S;aA, A;aA, A;bA, A;b")
    palabra = entrada_palabra.get()
    # palabras = ["aabb"]

    for palabra in palabra:
        pertenece = gramatica.generar_cadena(palabra)
        if pertenece:
            messagebox.showinfo(
                "Resultado", f'La palabra "{palabra}" pertenece al lenguaje.'
            )
            gramatica.graph_tree()
        else:
            messagebox.showinfo(
                "Resultado", f'La palabra "{palabra}" no pertenece al lenguaje.'
            )


# if __name__ == "__main__":
#     verificar_palabra()

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
boton_verificar = tk.Button(
    ventana, text="Verificar Palabra", command=verificar_palabra
)
boton_verificar.grid(row=5, columnspan=2)

# Ejecutar el bucle de eventos de la ventana
ventana.mainloop()
