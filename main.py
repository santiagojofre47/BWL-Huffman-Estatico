import heapq
from nodoHuffman import NodoHuffman
import heapq


# Función para construir el árbol de Huffman
def construir_arbol_huffman(lista_simbolos):
    # Crear una lista de nodos de Huffman y luego convertirla en una heap
    heap = [NodoHuffman(simbolo, frecuencia) for simbolo, frecuencia in lista_simbolos]
    heapq.heapify(heap)
    
    # Construimos el árbol combinando los nodos de menor frecuencia
    while len(heap) > 1:
        nodo_izq = heapq.heappop(heap)
        nodo_der = heapq.heappop(heap)
        
        # Crear un nuevo nodo combinando las frecuencias
        nuevo_nodo = NodoHuffman(nodo_izq.simbolo + nodo_der.simbolo, nodo_izq.frecuencia + nodo_der.frecuencia)
        nuevo_nodo.izquierda = nodo_izq
        nuevo_nodo.derecha = nodo_der
        
        # Añadir el nuevo nodo a la heap
        heapq.heappush(heap, nuevo_nodo)
    
    # El último nodo que queda es la raíz del árbol de Huffman
    return heap[0]

# Función para generar los códigos binarios recorriendo el árbol
def generar_codigos_huffman(nodo, codigo_actual="", codigos={}):
    if nodo is None:
        return
    
    # Si llegamos a un nodo hoja (con un símbolo), asignamos el código
    if len(nodo.simbolo) == 1:
        codigos[nodo.simbolo] = codigo_actual
    
    # Recursión para los subárboles
    generar_codigos_huffman(nodo.izquierda, codigo_actual + "0", codigos)
    generar_codigos_huffman(nodo.derecha, codigo_actual + "1", codigos)
    
    return codigos

#Obtener la cantidad de repeticiones por cada caracter de la cadena resultante
def getFrecuencias(cadena):
    frecuencias = []
    analizado = []
    for i in range(len(cadena)):
        if not analizado or cadena[i] not in analizado:
            cantidad = cadena.count(cadena[i])
            frecuencias.append((cadena[i], round(cantidad / len(cadena), 2)))
            analizado.append(cadena[i])
    return frecuencias


def getMatriz(cadena):
    n = len(cadena)
    lista = []
    lista.append(cadena)
    for i in range(n-1):
        # Tomar el último carácter
        c = cadena[-1]
        # Concatenar el último carácter al inicio y el resto de la cadena después
        cadena = c + cadena[:-1]
        lista.append(cadena)
    lista.sort()
    return lista

#Obtener la transformada BWT
def getTransformada(matriz,original):
    columna = ""
    r = 0
    for j in range(len(matriz)):
        columna += matriz[j][-1]
        if matriz[j] == original:
            r = j+1
    return (r,columna)



def generarComprimido(codificaciones,texto):
    comp = []
    res = ""
    for i in range(len(texto)):
        for simbolo,codigo in codificaciones.items():
            if texto[i] == simbolo:
                comp.append((simbolo,codigo))
                res += codigo
    return comp,res

def generDescompresion(codificaciones,comprimido):
    descomprimido = ""
    for i in range(len(comprimido)):
        for simbolo,codigo in codificaciones.items():
            if comprimido[i][1] == codigo:
                descomprimido+=comprimido[i][0]
    return descomprimido

# Invertir la transformada BWT
def reconstruirTextoBWT(columna, fila_original):
    # Paso 1: Obtener la primera columna ordenando los caracteres de la última columna
    primera_columna = sorted(columna)

    # Paso 2: Crear las correspondencias entre la primera y la última columna
    # Esto es, asociamos cada carácter de la última columna con su posición en la primera columna.
    n = len(columna)
    posiciones = [0] * n
    usados = {}
    
    for i in range(n):
        char = columna[i]
        # En cada carácter, aseguramos su aparición secuencial (si hay repeticiones)
        if char not in usados:
            usados[char] = 0
        else:
            usados[char] += 1

        # Encuentra la posición correspondiente en la primera columna
        pos = -1
        count = usados[char]
        for j in range(n):
            if primera_columna[j] == char:
                if count == 0:
                    pos = j
                    break
                count -= 1

        posiciones[i] = pos

    # Paso 3: Reconstruir la cadena original usando la fila original y las posiciones
    resultado = ""
    fila = fila_original - 1  # Ajustar a índice base 0

    for _ in range(n):
        resultado += columna[fila]
        fila = posiciones[fila]


    return resultado[::-1]

def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r') as archivo:  # 'r' es para leer el archivo
            contenido = archivo.read()  # Lee todo el contenido del archivo
        return contenido
    except FileNotFoundError:
        print("El archivo no fue encontrado.")
        return None
    
if __name__ == "__main__":
    texto = leer_archivo('entrada.txt')
    original = texto
    matriz = getMatriz(texto)
    transformada = getTransformada(matriz,original)
    probabilidades = getFrecuencias(transformada[1])
    arbol_huffman = construir_arbol_huffman(probabilidades)
    codificaciones = generar_codigos_huffman(arbol_huffman)
    print('Resultado de la transformación de BWT')
    print(transformada)
   #print(codificaciones.items())
    print("CODIFICACION DE HUFFMAN para la salida de BWT")
    for simbolo, codigo in codificaciones.items():
        print(f"Símbolo: {simbolo}, Código: {codigo}")
    comprimido,res = generarComprimido(codificaciones,transformada[1])
    print("Texto comprimido y codificado: ")
    print(res)
    print("Descompresión: ")
    descomprimido = generDescompresion(codificaciones,comprimido)
    print(descomprimido)
    print("Texto original regenerado:")
    print(reconstruirTextoBWT(descomprimido,transformada[0]))
 
