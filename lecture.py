

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

def writeOut(globalCost, globalTime, mejorSolucionGlobal, mejorCostoGlobal, name):
    file = open ( name[:2] + "_out.txt",'a')
    file.write("\n******************* Inicio de inserción ******************\n\n")
    file.write("Los elementos son del archivo: " + name)
    file.write("\n\nLos costos globales son: \n")
    for aux in globalCost:
        file.write(str(aux) + " ")
    file.write("\n\nLos tiempos globales son: \n\n")
    count = 1
    for aux in globalTime:
        file.write("Iteración " + str(count) + ": " + str(aux) + " \n")
        count = count + 1
    file.write("\nLa mejor solución global es: ")
    for aux in mejorSolucionGlobal:
        file.write(str(aux) + " ")
    file.write("\n\nEl mejor costo es: : ")
    file.write(str(mejorCostoGlobal) + " ")
    file.write("\n\n")
    file.write("******************* Termino de inserción ******************")
    file.write("\n")
    file.close()