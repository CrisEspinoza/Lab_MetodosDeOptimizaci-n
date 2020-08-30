import random
import copy
import matplotlib.pyplot as plt
from time import time
import numpy as np
import math

# Función que genera una solución aleatoria inicial
def generateInitialSolution(installation,numberToCreate):
	poblation = []
	if numberToCreate == 1:
		initialSolution = list(range(installation))
		random.shuffle(initialSolution)
		return initialSolution
	else:
		for count in range(numberToCreate):
			initialSolution = list(range(installation))
			random.shuffle(initialSolution)
			poblation.append(initialSolution)
		return poblation

# ------------------------------------------------------- # 
## Neighborhood

def generateAnotherNumber(lenSolution, numberOne):
	flag = True
	while flag:
		numberTwo = random.randint(0,lenSolution-1)
		if (numberOne != numberTwo):
			flag = False
	return numberTwo

def changeTwoPosition(solution):
	solution = solution
	numberOne = random.randint(0,len(solution)-1)
	numberTwo = generateAnotherNumber(len(solution),numberOne)
	aux = copy.copy(solution)
	aux = solution[numberOne]
	solution[numberOne] = solution[numberTwo]
	solution[numberTwo] = aux
	return solution

def theBestNeighborhood(solution,matrizF,matrizD):
	neighborhoods = []
	aux = list()
	for x in range(5):
		aux = copy.copy(changeTwoPosition(solution))
		neighborhoods.append(aux)
	valueObjectNeighborhood = [[objectFunction(neighborhoods[x],matrizF,matrizD),neighborhoods[x], neighborhoods[x]] for x in range(5)]
	valueObjectNeighborhood.sort(key = lambda x : x[0])
	aux = valueObjectNeighborhood[0][1]
	return aux

# ------------------------------------------------------- #
## Object Function 

# Calcula el valor de la funcion de la solución
def objectFunction(auxSolution, matrizF, matrizD):
	large = len(auxSolution)
	totalSum = 0
	for i in range(large):
		for j in range(large):
			totalSum = totalSum + matrizF[i,j] * matrizD[auxSolution[i],auxSolution[j]]
	return totalSum


# ------------- SA ------------------#

def SA(Tmax, Tmin, iteracionesInternas, alpha, initial, matrizF, matrizD,repeat):

	globalCost = []
	globalTime = []
	mejorSolucionGlobal = []
	mejorCostoGlobal = []
	for count in range(repeat):
	    start_time = time()
	    costos = []
	    mejorCostoGlobal = copy.copy(objectFunction(initial,matrizF,matrizD))
	    mejorCosto = copy.copy(objectFunction(initial,matrizF,matrizD))
	    costoActual = copy.copy(objectFunction(initial,matrizF,matrizD))
	    mejorSolucion = copy.copy(initial)
	    actualSolucion = copy.copy(initial)
	    mejorSolucionGlobal = copy.copy(initial)
	    Tact = copy.copy(Tmax)
	    while(Tact > Tmin):
	        for i in range(iteracionesInternas):
	            initial_prima = copy.copy(theBestNeighborhood(actualSolucion,matrizF,matrizD))
	            costoNew = copy.copy(objectFunction(initial_prima,matrizF,matrizD))
	            error = costoNew - costoActual
	            if error <= 0: 
	            	costoActual = copy.copy(costoNew)
	            	actualSolucion = copy.copy(initial_prima)
	            	if mejorCosto > costoNew:
	            		mejorSolucionGlobal = copy.copy(initial_prima)
	            		mejorCostoGlobal = copy.copy(costoNew)
	            		mejorCosto = copy.copy(costoNew)
	            		mejorSolucion = copy.copy(initial_prima)
	            elif random.random() < (math.e**(-(error)/Tact)):
	                actualSolucion = copy.copy(initial_prima)
	                costoActual = copy.copy(costoNew)
	            costos.append(costoActual)
	        Tact = alpha*Tact
	    elapsed_time = time() - start_time
	    globalCost.append(costos)
	    globalTime.append(elapsed_time)
	    print("Siguiente")
	graficarSA(globalCost)
	return globalCost, globalTime, mejorSolucionGlobal, mejorCostoGlobal


# --------------- Tournament ------------- # 

def tournament(initialPoblation,quantityOfParents,matrizF,matrizD):
	poblation = initialPoblation
	selectPoblation = []
	selectForCompetition = []
	objectFuntionList = []
	for count in range(quantityOfParents):
		index = np.random.choice(len(poblation),10,replace=True)
		selectForCompetition = [poblation[i] for i in index]
		objectFuntionList = [[objectFunction(selectForCompetition[i],matrizF,matrizD),selectForCompetition[i]] for i in range(len(selectForCompetition))]
		objectFuntionList.sort(key = lambda x : x[0])
		selectPoblation.append(objectFuntionList[0][1])
	return selectPoblation

# ----------------- Reproduction -------------- # 

def reproduction(selectPoblation):
	reproductionList = []
	auxReproduction = []
	for auxSolution in range(5):
		numberOne = random.randint(0,len(selectPoblation)-1)
		numberTwo = generateAnotherNumber(len(selectPoblation),numberOne)

		father1 = selectPoblation[numberOne]
		father2 = selectPoblation[numberTwo]
		son1 = [None]*len(father1)
		son2 = [None]*len(father2)

		# Son 1
			# Numeros para mantener iguales 
		start = random.randint(1,len(father1)-1)
		end = random.randint(start,len(father1)-1)
		
		for position in range(start,end):
			son1[position] = father1[position]
			son2[position] = father2[position]
	
		# Adding the other element
		for aux in range(start,end):
			if not(father2[aux] in son1):
				son1 = searhPosition(son1,father2,aux)
			if not(father1[aux] in son2):
				son2 = searhPosition(son2,father1,aux)
		for aux in range(len(father2)):
			if not(father2[aux] in son1):
				son1 = searhPosition(son1,father2,aux)
			if not(father1[aux] in son2):
				son2 = searhPosition(son2,father1,aux)
		reproductionList.append(son1)
		reproductionList.append(son2)
	return reproductionList

def searhPosition(son1,father2,auxEntrace):
	aux = copy.copy(auxEntrace)
	toAdd = copy.copy(father2[aux])
	flag = True
	while flag:
		if son1[aux] is None:
			son1[aux] = toAdd
			flag = False
		else:
			aux = copy.copy(father2.index(son1[aux]))
	return son1

# ------------------- Mutation -------------------- #

def mutation(reproductionList,porcentageOfMutation):
	mutationList = []
	for auxSolution in reproductionList:
		if (random.random() < porcentageOfMutation):
			mutationList.append(changeTwoPosition(auxSolution))
		else:
			mutationList.append(auxSolution)
	return mutationList

# ---------------- NewGenetation ---------------- #

def changeGeneration(oldPoblation,newGenetation,quantityOfGeneration,matrizF,matrizD):
	newGenetationFinal = []
	newGenetationSelected = []

	# 80% the best solution newGeneration
	newGenetation = [[objectFunction(newGenetation[i],matrizF,matrizD),newGenetation[i]] for i in range(len(newGenetation))]
	newGenetation.sort(key = lambda x : x[0])
	
	# 20% the best solucion oldGeneration
	oldPoblation = [[objectFunction(oldPoblation[i],matrizF,matrizD),oldPoblation[i]] for i in range(len(oldPoblation))]
	oldPoblation.sort(key = lambda x : x[0])

	newGenetationSelected.extend(newGenetation[:70])
	newGenetationSelected.extend(oldPoblation[:30])
	
	for solutionFinal in newGenetationSelected:
		newGenetationFinal.append(solutionFinal[1])
	return newGenetationFinal

# ------------------ TheBestForGeneration ------- # 

def theBestSolutionForGeneration(newGenetation,matrizF,matrizD):
	newGenetation = [[objectFunction(newGenetation[i],matrizF,matrizD),newGenetation[i]] for i in range(len(newGenetation))]
	newGenetation.sort(key = lambda x : x[0])
	return newGenetation[0]

# ---------- Genetico ------------------ # 

def AG(initialPoblation,matrizF,matrizD,generation,quantityOfParents,porcentageOfMutation,repeat):
	globalBetterSolution = []
	globalTime = []
	mejorSolucionGlobal = []
	mejorCostoGlobal = []

	for count in range(repeat):
		start_time = time()
		poblation = copy.copy(initialPoblation)  
		betterSolution = []
		betterSolution.append(theBestSolutionForGeneration(poblation,matrizF,matrizD)[0])
		mejorCostoGlobal = theBestSolutionForGeneration(poblation,matrizF,matrizD)[0]
		mejorSolucionGlobal = theBestSolutionForGeneration(poblation,matrizF,matrizD)[1]

		for actualGeneration in range(generation-1):
			selectPoblation = tournament(poblation,quantityOfParents,matrizF,matrizD)
			reproductionList = reproduction(selectPoblation)
			mutationList = mutation(reproductionList,porcentageOfMutation)
			poblation = changeGeneration(poblation,mutationList,len(poblation),matrizF,matrizD)
			# Save the best solution
			auxSolution = theBestSolutionForGeneration(poblation,matrizF,matrizD)
			betterSolution.append(auxSolution[0])
			if (mejorCostoGlobal > auxSolution[0]):
				mejorCostoGlobal = copy.copy(auxSolution[0])
				mejorSolucionGlobal = copy.copy(auxSolution[1])
			#betterSolution.append(theBestSolutionForGeneration(poblation,matrizF,matrizD))
		print(betterSolution)
		elapsed_time = time() - start_time
		globalBetterSolution.append(betterSolution)
		globalTime.append(elapsed_time)
		print("Iteracion " + str(count+1))
	graficarAG(globalBetterSolution,globalTime,generation,repeat)
	return globalBetterSolution, globalTime, mejorSolucionGlobal, mejorCostoGlobal


def graficarAG(globalBetterSolution,globalTime,generation,repeat):
	colors = ['black','red','gray','orange','gold','yellow','green','aqua','blue','indigo','pink']
	count = 0
	generation = list(range(1,generation+1))
	indexForTime = list(range(1,repeat+1))
	
	dateComplete = []
	for aux in range(len(globalBetterSolution)):
		listAux = []
		listAux.append(globalBetterSolution[aux])
		listAux.append(globalTime[aux])
		dateComplete.append(listAux)

	dateComplete.sort(key = lambda x : x[0][len(x[0])-1])

	for instancia in dateComplete:
		plt.scatter(generation,instancia[0],s=15)
	plt.title("Totalidad de ejecuciones")
	plt.ylabel("Costos")
	plt.xlabel("Generación")
	plt.legend(loc='best')
	plt.show()

	for instancia in dateComplete[:11]:
		plt.scatter(generation,instancia[0],c=colors[count],label="Iteración" + str(count+1),s=15)
		count = count + 1
	plt.title("Los 11 mejores resultados")
	plt.ylabel("Costos")
	plt.xlabel("Generación")
	plt.legend(loc='best')
	plt.show()

	count = 0
	for instancia in dateComplete[len(dateComplete[0])-11:]:
		plt.scatter(generation,instancia[0],c=colors[count],label="Iteración" + str(count+1),s=15)
		count = count + 1
	plt.title("Los 11 peores resultados")
	plt.ylabel("Costos")
	plt.xlabel("Generación")
	plt.legend(loc='best')
	plt.show()

	count = 0
	for instancia in dateComplete[:3]:
		plt.scatter(generation,instancia[0],c=colors[count],label="Iteración" + str(count+1),s=15)
		count = count + 1
	plt.title("Los 3 mejores resultados")
	plt.ylabel("Costos")
	plt.xlabel("Generación")
	plt.legend(loc='best')
	plt.show()

	auxTimeOrder = []
	for auxTime in dateComplete:
		auxTimeOrder.append(auxTime[1])
	plt.scatter(indexForTime,auxTimeOrder,s=15)
	plt.ylabel("Tiempo de ejecución de las instancias")
	plt.xlabel("Repetición")
	plt.legend(loc='best')
	plt.show()	


def graficarSA(globalBetterSolution):
	print(globalBetterSolution[0])
	print(str(len(globalBetterSolution[0])))
	globalBetterSolution.sort(key = lambda x : x[len(x)-1])
	print(globalBetterSolution)
	colors = ['black','red','gray','orange','gold','yellow','green','aqua','blue','indigo','pink']
	count = 0
	generation = list(range(1,len(globalBetterSolution[0])+1))

	for instancia in globalBetterSolution:
		plt.scatter(generation,instancia,s=15)
	plt.ylabel("Costos")
	plt.xlabel("Iteraciones")
	plt.legend(loc='best')
	plt.show()

	for instancia in globalBetterSolution[:11]:
		plt.scatter(generation,instancia,c=colors[count],label="Iteración" + str(count+1),s=15)
		count = count + 1
	plt.ylabel("Costos")
	plt.xlabel("Iteraciones")
	plt.legend(loc='best')
	plt.show()

	count = 0
	for instancia in globalBetterSolution[len(globalBetterSolution)-11:]:
		plt.scatter(generation,instancia,c=colors[count],label="Iteración" + str(count+1),s=15)
		count = count + 1
	plt.ylabel("Costos")
	plt.xlabel("Iteraciones")
	plt.legend(loc='best')
	plt.show()

	count = 0
	for instancia in globalBetterSolution[:3]:
		plt.scatter(generation,instancia,c=colors[count],label="Iteración" + str(count+1),s=15)
		count = count + 1
	plt.ylabel("Costos")
	plt.xlabel("Iteraciones")
	plt.legend(loc='best')
	plt.show()