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
        print(
            f"Derivando símbolo no terminal: {not_terminal}, palabra restante: {palabra}"
        )
        if not palabra:
            return True
        # print(not_terminal)
        print(self.producciones)
        if not_terminal in self.producciones:
            print("Entro")
            for produccion in self.producciones[not_terminal]:
                print("ENTRO AL FOR")
                print(
                    f"palabra: {palabra}, producción[0]: {produccion[0]}, produccion_normal: {produccion}"
                )
                if palabra.startswith(produccion[0]):
                    print(
                        f"Coincidencia encontrada: Producción: {produccion}, Palabra actual: {palabra}"
                    )
                    if self.derivar(produccion[1:], palabra[1:]):
                        print("if final")
                        return True

        return False


def verificar_palabra():
    gramatica = Gramatica("a, b", "S, A", "S", "S;aA, A;aA, A;bA, A;b")

    palabras = ["aaab"]

    for palabra in palabras:
        pertenece = gramatica.generar_cadena(palabra)
        if pertenece:
            print(f'La palabra "{palabra}" pertenece al lenguaje.')
        else:
            print(f'La palabra "{palabra}" no pertenece al lenguaje.')


if __name__ == "__main__":
    verificar_palabra()
