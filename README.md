Se dividio el programa en dos módulos: encode.py y decode.py. Ahora al generar la compresión del archvo se generará un archivo .bin (archivo binario) de salida. Este contendrá una cabecera con el numero de fila de la salida de la transformada BWT, otra cabecera que guarda las codificaciones de Huffman Estático, y luego el contenido que es la secuencia binaria asociada al texto comprimido.

Debido a las cabeceras, si el texto es corto, se notará una expansión ya que el tamaño del archivo de salida será mayor al archivo de entrada, pero si el texto es largo se verá reflejada la compresión.
Un problema que se presenta, es que si el texto contiene letras con tildes en la decodificación se interpretará como caracteres extraños, entonces el texto reconstruido será diferente al de entrada. En el archivo de entrada "Entrada.txt" se muestra un texto sin tildes

Para ejecutar, hacerlo desde main.py
