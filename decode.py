class Decode:
    #GenerarDescomprensión del archivo
    def descomprimir(self,tabla_huffman, secuencia_binaria):
        #Invertir la tabla de Huffman
        tabla_invertida = {codigo: caracter for caracter, codigo in tabla_huffman.items()}
        #print("Tabla invertida para descompresión:", tabla_invertida)  # Para verificar la tabla invertida

        texto_descomprimido = []
        codigo_actual = ""
    
        # Recorrer la secuencia binaria y descomprimir
        for bit in secuencia_binaria:
            codigo_actual += bit
            if codigo_actual in tabla_invertida:
                # Encontramos un carácter, agregamos a la lista de salida
                texto_descomprimido.append(tabla_invertida[codigo_actual])
               # print(f"Encontrado: {codigo_actual} -> {tabla_invertida[codigo_actual]}")  # Depuración
                codigo_actual = ""  # Reiniciar el código actual

        # Unir todos los caracteres para formar el texto descomprimido completo
        resultado = ''.join(texto_descomprimido)
        #print("Texto descomprimido:", resultado)  # Depuración final
        return resultado


    
    # Invertir la transformada BWT
    def reconstruirTextoBWT(self,columna, fila_original):
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
    
    def start(self,comprimido,codificaciones,numero_fila):
        descomprimido = self.descomprimir(codificaciones,comprimido)
        original = self.reconstruirTextoBWT(descomprimido,numero_fila)
        print("Descompresión: ")
        print(descomprimido)
        print("Texto original de entrada decodificado: ")
        print(original)
