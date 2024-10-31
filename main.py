from encode import Encode
from decode import Decode

if __name__ == "__main__":
    objEncoder = Encode("entrada.txt","salida.bin")
    objDecoder = Decode()
    comprimido,codificaciones,numero_fila = objEncoder.start()
    objDecoder.start(comprimido,codificaciones,numero_fila)
