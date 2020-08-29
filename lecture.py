

# Función que se encarga de leer el archivo.
def lectureFile(name):
    archivo = open("Archivos/" + name,'r')
    matriz = [] 
    fila = []
    for linea in archivo:
        fila = linea.split()
        filaInt = []
        for elemento in fila:
            filaInt.append(int(elemento))
        matriz.append(filaInt)
    archivo.close()
    return matriz