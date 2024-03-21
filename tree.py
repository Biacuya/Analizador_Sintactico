class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, index):
        del self.children[index]

    def get_children(self):
        return self.children


class DerivationTree:
    def __init__(self, initial_symbol):
        self.root = TreeNode(initial_symbol)

    def add_node(self, parent, data):
        new_node = TreeNode(data)
        parent.add_child(new_node)
        return new_node

    def remove_node(self, parent, index):
        parent.remove_child(index)

    def get_root(self):
        return self.root


# Ejemplo de uso:
derivation_tree = DerivationTree("S")  # Crear un árbol con el símbolo inicial "S"
root = derivation_tree.get_root()  # Obtener el nodo raíz

# Agregar nodos hijos
A = derivation_tree.add_node(root, "A")
B = derivation_tree.add_node(root, "B")

# Agregar nodos nietos
derivation_tree.add_node(A, "a")
derivation_tree.add_node(B, "b")

# Agregar más nodos si es necesario...

# Obtener hijos de un nodo
children = root.get_children()
for child in children:
    print(child.data)
Gramatica("a, b", "S, A, B", "S", "S;aA, A;aA, A;bA, A;b")