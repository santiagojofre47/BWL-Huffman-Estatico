# Clase Nodo para construir el árbol de Huffman
class NodoHuffman:
    def __init__(self, simbolo, frecuencia):
        self.simbolo = simbolo  # Puede ser un símbolo individual o un conjunto de símbolos
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    # Definir cómo comparar nodos (necesario para usar heapq)
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia
