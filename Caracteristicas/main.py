import ast
import numpy as np
import statistics as s

def tranferToList(name):
	archivo = open( name + ".txt",'r')
	archivo = archivo.read()
	archivo = archivo.replace('[',',[')
	archivo = "[" + archivo[1:] + "]"
	lista = ast.literal_eval(archivo)
	return lista

def lectureTime():
	archivo = open("Times.txt",'r')
	count = 0
	auxCount = 0
	listFinaly = []
	listAux = []
	for aux in archivo:
		aux1 = aux.replace("Iteración ","")[2:]
		aux1 = aux1.replace("\n","").replace(" ","").replace(":","")
		listAux.append(float(aux1))
		if auxCount == 31:
			listFinaly.append(listAux)
			listAux = []
			auxCount = -1
			count = count + 1
		auxCount = auxCount + 1
	return listFinaly

def caracteristic(arreglo):
	matrizNumpy = np.matrix(arreglo)
	listAux = []
	listAux.append(np.amin(matrizNumpy))
	listAux.append(np.amax(matrizNumpy))
	listAux.append(np.mean(matrizNumpy))
	listAux.append(np.std(matrizNumpy))
	listAux.append(np.var(matrizNumpy))
	return listAux

def valueForTime(arreglo,time):
	listFinaly = []
	matrizNumpy = np.matrix(arreglo)
	count = 0 
	for colum in matrizNumpy:
		listAux = []
		listAux.append(np.amin(colum))
		listAux.append(float(time[count]))
		listFinaly.append(listAux)
		count = count + 1
	listFinaly.sort(key = lambda x : x[0])
	return listFinaly

def caracteristicForTime(times):
	listFinalyTimes = [] # menor # mayor # promedio
	for time in times:
		listAux = []
		listAux.append(min(time))
		listAux.append(max(time))
		listAux.append(s.mean(time))
		listFinalyTimes.append(listAux)
	return listFinalyTimes


def writeFile(caracteristic,times):
	file = open ("outFinaly",'a')
	file.write("\n")
	file.write("\n******************* Inicio de inserción ******************\n\n")
	file.write("Los elementos son del archivo: " + caracteristic[0])
	file.write("\n")
	if "sa" in caracteristic[0]:
		file.write("La temperatura inicial es: " + str(float(caracteristic[1][1]) / 2))
		file.write("\n")
		if "64" in caracteristic[0]:
			file.write("La cantidad de iteraciones es: " + str(50))
		else:
			file.write("La cantidad de iteraciones es: " + str(100))
		file.write("\n")
		file.write("El valor de alpha es: " + str(0.99))
		file.write("\n")
	if "ag" in caracteristic[0]:
		if "64" in caracteristic[0] or "32" in caracteristic[0]:
			file.write("La población inicial es: " + str(100))
			file.write("\n")
			file.write("La cantidad de generacion es: " + str(100))
			file.write("\n")
			file.write("La cantidad de padres a generar es: " + str(50))
			file.write("\n")
		else:
			file.write("La población inicial es: " + str(200))
			file.write("\n")
			file.write("La cantidad de generacion es: " + str(200))
			file.write("\n")
			file.write("La cantidad de padres a generar es: " + str(100))
			file.write("\n")
		file.write("El porcentaje de mutacion es: " + str(0.1))
		file.write("\n")
	file.write("El valor minimo alcanzado fue: " + str(caracteristic[1][0]))
	file.write("\n")
	file.write("El valor minimo fue alcanzado en un tiempo de: " + str(times[0]))
	file.write("\n")
	file.write("El valor maximo alcanzado fue: " + str(caracteristic[1][1]))
	file.write("\n")
	file.write("El valor maximo fue alcanzado en un tiempo de: " + str(times[1]))
	file.write("\n")
	file.write("El valor medio alcanzado fue: " + str(caracteristic[1][2]))
	file.write("\n")
	file.write("El valor promedio en tiempos de ejecución fue de: " + str(times[2]))
	file.write("\n")
	file.write("El valor de la desviación estandar alcanzado fue: " + str(caracteristic[1][3]))
	file.write("\n")
	file.write("El valor de la varianza alcanzado fue: " + str(caracteristic[1][4]))
	file.write("\n\n")
	file.write("******************* Termino de inserción ******************")
	file.close()


def main():
	times = lectureTime()
	listFinaly = []
	listFinalyTimes = []
	arreglos = []
	names = ["12sa","26sa","32sa","64sa","12ag","26ag","32ag","64ag"]
	count = 0
	for name in names:
		print("Leyendo " + str(count+1))
		arreglos.append(tranferToList(name))
		count = count + 1
	count = 0
	for file in arreglos:
		print("Procesando " + str(count+1))
		listFinaly.append([names[count],caracteristic(file)])
		listFinalyTimes.append(valueForTime(file,times[count]))
		count = count + 1
	caracteristicTime = caracteristicForTime(times)
	count = 0
	for auxListFinaly in listFinaly:
		print("Escribiendo " + str(count+1))
		writeFile(auxListFinaly,caracteristicTime[count])
		count = count + 1

main()