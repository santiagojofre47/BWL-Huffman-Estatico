import os
import heapq
import struct
from nodoHuffman import NodoHuffman

class Encode:
    __rutaArchivo: str
    __rutaSalida: str

    def __init__(self, rutaArchivo,rutaSalida):
        self.__rutaArchivo = rutaArchivo
        self.__rutaSalida = rutaSalida

    def leer_archivo(self):
        try:
            with open(self.__rutaArchivo, 'r') as archivo:  # 'r' es para leer el archivo
                contenido = archivo.read()  # Lee todo el contenido del archivo
            return contenido
        except FileNotFoundError:
            print("El archivo no fue encontrado.")
        return None
    
    # Función para construir el árbol de Huffman
    def construir_arbol_huffman(self,lista_simbolos):
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
    def generar_codigos_huffman(self,nodo, codigo_actual="", codigos={}):
        if nodo is None:
            return
        # Si llegamos a un nodo hoja (con un símbolo), asignamos el código
        if len(nodo.simbolo) == 1:
            codigos[nodo.simbolo] = codigo_actual
        # Recursión para los subárboles
        self.generar_codigos_huffman(nodo.izquierda, codigo_actual + "0", codigos)
        self.generar_codigos_huffman(nodo.derecha, codigo_actual + "1", codigos)
        return codigos
    
    #Obtener la cantidad de repeticiones por cada caracter de la cadena resultante
    def getFrecuencias(self,cadena):
        frecuencias = []
        analizado = []
        for i in range(len(cadena)):
            if not analizado or cadena[i] not in analizado:
                cantidad = cadena.count(cadena[i])
                frecuencias.append((cadena[i], round(cantidad / len(cadena), 2)))
                analizado.append(cadena[i])
        return frecuencias
    
    def getMatriz(self,cadena):
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
    def getTransformada(self,matriz,original):
        columna = ""
        r = 0
        for j in range(len(matriz)):
            columna += matriz[j][-1]
            if matriz[j] == original:
                r = j+1
        return (r,columna)

    def comprimir_texto(self,texto, codigos):
        texto_comprimido = "".join([codigos[caracter] for caracter in texto])
        return texto_comprimido

    def escribir_archivo_con_cabecera(self, tabla_huffman, secuencia_binaria,numero_fila):
        with open(self.__rutaSalida, 'wb') as archivo_bin:
            archivo_bin.write(struct.pack('I', numero_fila))
            archivo_bin.write(len(tabla_huffman).to_bytes(1, byteorder='big'))
            # Escribir cada carácter y su código en la cabecera
            for caracter, codigo in tabla_huffman.items():
                # Escribir el carácter
                archivo_bin.write(caracter.encode('latin1'))  # Codifica el carácter como un solo byte
            
                # Escribir la longitud del código
                longitud_codigo = len(codigo)
                archivo_bin.write(longitud_codigo.to_bytes(1, byteorder='big'))
            
                # Convertir el código de Huffman en una secuencia de bytes
                num_bytes = (longitud_codigo + 7) // 8  # Número de bytes necesarios
                codigo_bytes = int(codigo, 2).to_bytes(num_bytes, byteorder='big')
                archivo_bin.write(codigo_bytes)
        
            # Guardar la longitud del último bloque de bits válidos
            longitud_ultimo_bloque = len(secuencia_binaria) % 8 or 8
            archivo_bin.write(longitud_ultimo_bloque.to_bytes(1, byteorder='big'))
        
            # Convertir secuencia binaria a bytes
            bytes_comprimidos = bytearray()
            for i in range(0, len(secuencia_binaria), 8):
                byte = secuencia_binaria[i:i+8]
                bytes_comprimidos.append(int(byte, 2))
        
            # Escribir la secuencia binaria comprimida
            archivo_bin.write(bytes(bytes_comprimidos))

    
    def leer_archivo_con_cabecera(self):
        with open(self.__rutaSalida, 'rb') as archivo_bin:
            #Lee la primer cabecera del archivo que contendrá el número de fila de la transformada BWT, que servira para despúes reconstruir el texto original
            numero_fila = struct.unpack('I', archivo_bin.read(4))[0]

            # Leer el número de caracteres en la tabla
            numero_caracteres = int.from_bytes(archivo_bin.read(1), byteorder='big')
            # # Reconstruir la tabla de Huffman desde la cabecera
            tabla_huffman = {}
            # Leer los caracteres y sus códigos binarios
            for _ in range(numero_caracteres):
                # Leer el carácter
                caracter = archivo_bin.read(1).decode('latin1')
                longitud_codigo = int.from_bytes(archivo_bin.read(1), byteorder='big')  # Longitud del código en bits
            
                # Calcular el número de bytes necesarios para el código
                num_bytes = (longitud_codigo + 7) // 8
                codigo_bytes = archivo_bin.read(num_bytes)
                # Convertir bytes a binario y ajustar longitud
                codigo = bin(int.from_bytes(codigo_bytes, byteorder='big'))[2:].zfill(longitud_codigo)
                tabla_huffman[caracter] = codigo
        
            # Leer la cantidad de bits válidos del último byte
            longitud_ultimo_bloque = int.from_bytes(archivo_bin.read(1), byteorder='big')
        
            # Leer la secuencia comprimida en bytes
            bytes_comprimidos = archivo_bin.read()
        
            # Convertir los bytes leídos a una cadena binaria completa
            secuencia_binaria = ''.join(f'{byte:08b}' for byte in bytes_comprimidos)
        
            # Eliminar bits de relleno si es necesario
            if longitud_ultimo_bloque < 8:
                secuencia_binaria = secuencia_binaria[:-(8 - longitud_ultimo_bloque)]
        
        return tabla_huffman, secuencia_binaria, numero_fila
        

    def start(self):
        cadena = self.leer_archivo()
        original = cadena
        matriz = self.getMatriz(cadena)
        transformada = self.getTransformada(matriz,original)
        probabilidades = self.getFrecuencias(transformada[1])
        arbolHuffman = self.construir_arbol_huffman(probabilidades)
        codificaciones = self.generar_codigos_huffman(arbolHuffman)
        print("CODIFICACION DE HUFFMAN para la salida de BWT")
        for simbolo, codigo in codificaciones.items():
            print(f"Símbolo: {simbolo}, Código: {codigo}")
        res = self.comprimir_texto(transformada[1],codificaciones)
        print("Texto comprimido y codificado: ")
        self.escribir_archivo_con_cabecera(codificaciones,res,transformada[0])
        print(res)
        print("Tamaño texto original: {} bytes" .format(os.path.getsize(self.__rutaArchivo)))
        print("Tamaño archivo comprimido: {} bytes".format(os.path.getsize(self.__rutaSalida)))
        tabla,secuencia_binaria,numero_fila = self.leer_archivo_con_cabecera()
        return secuencia_binaria,tabla,numero_fila
    

