from lecture import lectureFile, writeOut
from solutions import generateInitialSolution,objectFunction,theBestNeighborhood, SA, AG
import numpy

def menu ():

	opcion = 0
	matrixFlow = None
	matrixDistance = None

	while opcion != 4:

		print("1. Ingresar archivo")
		print("2. Realizar análisis SA")
		print("3. Realizar análisis AG")
		print("4. Salir")

		opcion = input("Ingrese la opción: ")
		print(opcion)
		if opcion == "1":
			#name = input("Ingrese el nombre del archivo (con extensión): ")
			name = "12.txt"
			# Matriz de instalaciones
			matrixFlow = numpy.array(lectureFile("F" + name))
			# Matriz de distancias
			matrixDistance = numpy.array(lectureFile("D" + name))

		elif opcion == "2" and matrixFlow is not None and matrixDistance is not None:
			initialSolution = generateInitialSolution(len(matrixFlow),1)
			maxTemperature = objectFunction(initialSolution,matrixFlow,matrixDistance)/2
			minTemperature = 10
			numberOfIteration = 1 # 50 para 64 
			alpha = 0.99 # Geometrica
			globalCostSA, globalTimeSA, mejorSolucionGlobalSA, mejorCostoGlobalSA = SA(maxTemperature,minTemperature,numberOfIteration,alpha,initialSolution,matrixFlow,matrixDistance,1)
			writeOut(globalCostSA, globalTimeSA, mejorSolucionGlobalSA, mejorCostoGlobalSA,name[:2] + "_SA")

		elif opcion == "3" and matrixFlow is not None and matrixDistance is not None:
			numberOfPoblation = 200
			porcentageOfMutation = 0.1
			quantityOfParents = int(numberOfPoblation/2)
			quantityOfGeneration = 200
			poblation = generateInitialSolution(len(matrixFlow),numberOfPoblation)
			globalCostAG, globalTimeAG, mejorSolucionGlobalAG, mejorCostoGlobalAG = AG(poblation,matrixFlow,matrixDistance,quantityOfGeneration,quantityOfParents,porcentageOfMutation,32)
			writeOut(globalCostAG, globalTimeAG, mejorSolucionGlobalAG, mejorCostoGlobalAG,name[:2] + "_AG")
			print("Opcion 3")
		
		elif opcion == "4":
			print("Opcion 4")
			opcion = 4

		elif matrixFlow is None or matrixDistance is None:
			print("Primero debe cargar un archivo ")

		else:
			print("Ingrese una opcion valida")

		print("\n\n")
menu()