from graphviz import Digraph
import os

os.environ["PATH"] += os.pathsep + "C:/Users/byacu/Downloads/Graphviz-10.0.1-win64/bin"


class node:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def node_get_value(self):
        return self.value

    def node_get_name(self):
        return self.name


# Crear un nuevo gráfico dirigido
class Graphic_tree:
    dot = Digraph()

    def create_graphic_horinzontal(cls, value, name, start_node, end_node):
        new_node = node(value, name)

        cls.dot.node(new_node.node_get_value(), new_node.node_get_name())
        cls.dot.edges([(start_node, end_node)])
        cls.dot.render("arbol_pruebas_horizontal", format="png", cleanup=True)
        # print("Nodo creado")

    def render_tree(cls):
        cls.dot.render("arbol_pruebas_vertical", format="png", cleanup=True)
