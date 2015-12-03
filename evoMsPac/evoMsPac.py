#Author: Michael Kammeyer

import sys
import Ghost
import MsPac
import State
import time
import datetime
import random

#Returns the move for Ms. Pacman to make
def chooseMove(moves, state):
	best = "STAY"
	bestRank = state.rank
	for move in moves:
		if move == "LEFT":
			tempState = state
			tempState.msPac.locationX -= 1
			tempState.evaluateState()
			if tempState.rank > bestRank:
				best = move
				bestRank = tempState.rank
		if move == "RIGHT":
			tempState = state
			tempState.msPac.locationX += 1
			tempState.evaluateState()
			if tempState.rank > bestRank:
				best = move
				bestRank = tempState.rank
		if move == "UP":
			tempState = state
			tempState.msPac.locationY -= 1
			tempState.evaluateState()
			if tempState.rank > bestRank:
				best = move
				bestRank = tempState.rank
		if move == "DOWN":
			tempState = state
			tempState.msPac.locationY += 1
			tempState.evaluateState()
			if tempState.rank > bestRank:
				best = move
				bestRank = tempState.rank
	return best

#Takes a state, runs a game from start to finish, calculating the score.
#Also returns a world string to write to a file if the score is best so far
def runGame(state):
	#Initial World Log
	tempWorld = ""
	tempWorld += str(state.width) + "\n"
	tempWorld += str(state.height) + "\n"
	tempWorld += "m" + " " + str(state.msPac.locationX) + " " + str(state.msPac.locationY) + "\n"
	for k in range(0, len(state.ghosts)):
		tempWorld += str(k+1) + " " + str(state.ghosts[k].locationX) + " " + str(state.ghosts[k].locationY) + "\n"
	for k in range(0, len(state.pills)):
		tempWorld += "p" + " " + str(state.pills[k].x) + " " + str(state.pills[k].y) + "\n"
	tempWorld += "t" + " " + str(state.time) + " " + str(state.score) + "\n"

	#Run the game
	gameOver = False
	while not gameOver:
		moves = state.msPac.getValidMoves(state)
		move = chooseMove(moves, state)

		#Update the board
		state.step(move)

		#World Log
		tempWorld += "m" + " " + str(state.msPac.locationX) + " " + str(state.msPac.locationY) + "\n"
		for k in range(0, len(state.ghosts)):
			tempWorld += str(k+1) + " " + str(state.ghosts[k].locationX) + " " + str(state.ghosts[k].locationY) + "\n"
		tempWorld += "t" + " " + str(state.time) + " " + str(state.score) + "\n"
		
		#Check if game is over
		gameOver = state.isGameOver()

	return state, tempWorld

#Chooses Parents, combines or mutates them to create children, evaluates them, and adds them to the population
def createChildren(population, genSize, bestOverallScore, worldFile, solFile, pDensity, maxDepth, p, parentSelection):
	children = []
	for i in range(0, genSize):
		#Choose Parents
		rand = random.randrange(0, 2)
		if rand == 0:
			parents = chooseParents(population, parentSelection, 2)
			tree = combine(parents)

			msPac = MsPac.MsPac()
			msPac.tree = tree
			child = State.State(parents[0].width, parents[0].height, parents[0].ghosts, msPac, pDensity)

		else:
			parents = chooseParents(population, parentSelection, 1)
			tree = parents[0].msPac.tree
			msPac = MsPac.MsPac()
			msPac.tree = tree
			child = State.State(parents[0].width, parents[0].height, parents[0].ghosts, msPac, pDensity)
		
		child.generateGrid(pDensity)
		child, tempWorld = runGame(child)
		child = penalty(child, p, maxDepth)
		if child.score > bestOverallScore:
			#Log the world file if best overall
			bestOverallScore = child.score
			world = open(worldFile, 'w')
			world.write(tempWorld)
			world.close() 

			solution = open(solFile, 'w')
			solution.write(child.msPac.tree.printOut(1))
			solution.close()
		children.append(child)

	population.extend(children)
	return population, bestOverallScore

#Returns a given number of parents using either overselection or fitness proportional selection.
def chooseParents(population, parentSelection, num):
	parents = []
	if parentSelection == "OVERSELECTION":
		population.sort(key=lambda x: x.score)
		s1 = []
		s2 = []
		x = len(population) - 1
		while (float(len(s1))/len(population))*100 < 32:
			s1.append(population[x])
			x -= 1

		while x >= 0:
			x-=1
			s2.append(population[x])

		for i in range(0, num):
			rand = random.randrange(1, 101)
			if rand < 80:
				parents.append(s1.pop(0))
			else:
				parents.append(s2.pop(0))

	else:
		for i in range(0, num):
			total = totalFitness(population)
			count = 0
			if total == 0:
				rand = random.randrange(0, len(population))
				parents.append(population[rand])
			else:
				rand = random.randrange(0, total)
				for state in population:
					count += state.score
					if count > rand:
						parents.append(state)
						break

	return parents

#returns a combination of two parents
def combine(parents):
	tree = parents[0].msPac.tree
	tree = tree.combine(parents[1].msPac.tree)
	# child = State.state(width, height, ghosts, msPac, pDensity)
	return tree

#returns a mutation of one parent.
def mutate(state):
	state.msPac.tree = state.msPac.tree.mutate()
	return state

#Runs survival selection till population is back to size, either using k-tournament or truncation.
def cutLosers(population, size, k):
	if k == 0:
		population.sort(key=lambda x: x.score)
		while len(population) > size:
			population.pop(0)

	else:
		while len(population) > size:
			indexes = random.sample(range(0, len(population)), k)
			tournament = []
			for j in indexes:
			    tournament.append(population[j])
			leastFitIndex = worstIndex(tournament)
			population.pop(indexes[leastFitIndex])

	return population

#Penalizes the score of a completed state if the controller it uses is too large.
def penalty(state, p, maxDepth):
	threshold = 0
	for i in range(0, maxDepth):
		threshold+=i

	size = len(state.msPac.tree.wholeTree())
	if size > threshold:
		state.score -= p*(size - threshold)

	return state

#Returns sum of all fitnesses in the population
def totalFitness(population):
	total = 0
	for state in population:
		total += state.score
	return total 

#Returns the best fitness in the population
def bestFitness(population):
	best = 0
	for state in population:
		if state.score > best:
			best = state.score
	return best

#Returns the average fitness in the population
def averageFitness(population):
	avg = 0
	for state in population:
		avg += state.score
	avg = avg/len(population)
	return avg 

#Returns the index of the state in the population with the lowest fitness.
def worstIndex(population):
	worst = population[0]
	index = 0
	for i in range(1, len(population)):
		if population[i].score < worst:
			worst = population[i].score
			index = i
	return index

#Main Scripts
def main():
	#Checks arguments for given config file, defaults to 1.cfg
	if len(sys.argv) > 1:
		config = open(sys.argv[1], 'r')
	else:
		config = open('config/1.cfg', 'r')

	#read in config values
	width = int(config.readline().split()[1])
	height = int(config.readline().split()[1])
	pDensity = int(config.readline().split()[1])
	seed = int(config.readline().split()[1])
	popSize = int(config.readline().split()[1])
	genSize = int(config.readline().split()[1])
	maxDepth = int(config.readline().split()[1])
	parentSelection = config.readline().split()[1]
	k = int(config.readline().split()[1])
	p = int(config.readline().split()[1])
	numEvals = int(config.readline().split()[1])
	runs = int(config.readline().split()[1])
	n = int(config.readline().split()[1])
	logFile = config.readline().split()[1]
	worldFile = config.readline().split()[1]
	solFile = config.readline().split()[1]

	#seed Random
	current_time = time.mktime(datetime.datetime.now().timetuple())
	if seed == 0:
		seed = current_time
	random.seed(seed)

	#open files
	log = open(logFile, 'w')

	#log headers
	log.write("Number of Runs: " + str(runs))
	log.write("\nNumber of Evals: " + str(numEvals))
	log.write("\nWorld height: " + str(height))
	log.write("\nWorld width: " + str(width))
	log.write("\nPill Density: " + str(pDensity))
	log.write("\nRandom Seed: " + str(seed))
	log.write("\nPopulation Size: " + str(popSize))
	log.write("\nGeneration Size: " + str(genSize))
	log.write("\nMax Tree Depth: " + str(maxDepth))
	if parentSelection == "OVERSELECTION":
		log.write("\nUsing Overselection Parent Selection")
	else:
		log.write("\nUsing Fitness Proportional Parent Selection")
	if k != 0:
		log.write("\nUsing K-Tournament Survivor Selection, k: " + str(k))
	else:
		log.write("\nUsing Truncation Survivor Selection")
	log.write("\nParsimony Pressure Constant: " + str(p))
	if n != 0:
		log.write("\nUsing N-Convergence, n: " + str(n))
	log.write("\nSolution File: " + str(solFile))
	log.write("\nWorld File: " + str(worldFile))
	log.write("\n\nResults Log")
	log.write("\n---------------\n\n")

	#begin runs
	bestOverallScore = 0
	for i in range(0, runs):
		log.write("Run " + str(i+1) + "\n")
		bestScore = 0
		evals = 0

		#initialize population, ramp half and half
		#First full trees
		population = []
		for j in range(0, popSize/2):
			msPac = MsPac.MsPac()
			msPac.generateFullTree(maxDepth)
			
			ghosts = []
			for i in range(0, 3):
				ghosts.append(Ghost.Ghost())

			state = State.State(width, height, ghosts, msPac, pDensity)
			state.generateGrid(pDensity)

			state, tempWorld = runGame(state)

			population.append(state)

			if state.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = state.score
				world = open(worldFile, 'w')
				world.write(tempWorld)
				world.close() 

				solution = open(solFile, 'w')
				solution.write(state.msPac.tree.printOut(1))
				solution.close()

		#Then Grow trees
		for j in range(popSize/2, popSize):
			msPac = MsPac.MsPac()
			msPac.generateGrowTree(maxDepth)
			
			ghosts = []
			for i in range(0, 3):
				ghosts.append(Ghost.Ghost())

			state = State.State(width, height, ghosts, msPac, pDensity)
			state.generateGrid(pDensity)

			state, tempWorld = runGame(state)

			population.append(state)

			if state.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = state.score
				world = open(worldFile, 'w')
				world.write(tempWorld)
				world.close() 

				solution = open(solFile, 'w')
				solution.write(state.msPac.tree.printOut(1))
				solution.close()

		#Calculates bests and averages for initial population
		evals += len(population)
		avgScore = averageFitness(population)
		bestScore = bestFitness(population)
		log.write(str(evals) + "\t" + str(avgScore) + "\t" + str(bestScore) + "\n")	
		terminate = False
		previousBest = bestScore
		tillConverge = n

		#Runs a generation while termination criteria is not met.
		while not terminate:
			#Create Children
			population, bestOverallScore = createChildren(population, genSize, bestOverallScore, worldFile, solFile, pDensity, maxDepth, p, parentSelection)
			
			#Survival Selection
			population = cutLosers(population, popSize, k)
			
			#Update number of evals
			evals += genSize

			#Log
			avgScore = averageFitness(population)
			bestScore = bestFitness(population)
			log.write(str(evals) + "\t" + str(avgScore) + "\t" + str(bestScore) + "\n")
			
			#Checks convergence criteria
			tillConverge -= 1
			if n != 0:
				if bestScore > previousBest:
					tillConverge = n
					previousBest = bestScore
				elif tillConverge == 0:
					terminate = True

			#Checks number of evals
			if evals >= numEvals:
				terminate = True
		log.write("\n")
	log.close()

if __name__ == "__main__":
	main()