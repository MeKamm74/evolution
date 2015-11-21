import sys
import Ghost
import MsPac
import State
import time
import datetime
import random

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

def createChildren(population, genSize, bestOverallScore, worldFile, pDensity):
	children = []
	for i in range(0, genSize):
		#Choose Parents
		parents = chooseParents(population)

		tree = combine(parents)

		msPac = MsPac.MsPac()
		msPac.tree = tree
		child = State.State(parents[0].width, parents[0].height, parents[0].ghosts, msPac, pDensity)

		child = mutate(child)
		
		child.generateGrid(pDensity)
		child, tempWorld = runGame(child)

		if child.score > bestOverallScore:
			#Log the world file if best overall
			bestOverallScore = child.score
			world = open(worldFile, 'w')
			world.write(tempWorld)
			world.close() 
		children.append(child)

	population.extend(population)
	return population

def chooseParents(population):
	parents = []
	for i in range(0, 2):
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

def combine(parents):
	tree = parents[0].msPac.tree
	tree = tree.combine(parents[1].msPac.tree)
	# child = State.state(width, height, ghosts, msPac, pDensity)
	return tree

def mutate(state):
	state.msPac.tree = state.msPac.tree.mutate()
	return state

def cutLosers(population, size):
	population.sort(key=lambda x: x.score)
	while len(population) > size:
		population.pop(0)

	return population

def totalFitness(population):
	total = 0
	for state in population:
		total += state.score
	return total 

def bestFitness(population):
	best = 0
	for state in population:
		if state.score > best:
			best = state.score
	return best

def averageFitness(population):
	avg = 0
	for state in population:
		avg += state.score
	avg = avg/len(population)
	return avg 

def worstIndex(population):
	worst = population[0]
	index = 0
	for i in range(1, len(population)):
		if population[i].score < worst:
			worst = population[i].score
			index = i
	return index

def main():
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
	k = int(config.readline().split()[1])
	p = int(config.readline().split()[1])
	numEvals = int(config.readline().split()[1])
	runs = int(config.readline().split()[1])
	logFile = config.readline().split()[1]
	worldFile = config.readline().split()[1]

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
	log.write("\nRandom Seed " + str(seed))
	log.write("\n\nResults Log")
	log.write("\n---------------\n\n")

	#begin runs
	bestOverallScore = 0
	for i in range(0, runs):
		log.write("Run " + str(i+1) + "\n")
		bestScore = 0
		evals = 0
		#initialize population, ramp half and half
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

		evals += len(population)
		avgScore = averageFitness(population)
		bestScore = bestFitness(population)
		log.write(str(evals) + "\t" + str(avgScore) + "\t" + str(bestScore) + "\n")	
			
		while evals < numEvals:
			#Create Children
			population = createChildren(population, genSize, bestOverallScore, worldFile, pDensity)
			
			#Cut Losers
			population = cutLosers(population, popSize)
			evals += genSize

			#Log
			avgScore = averageFitness(population)
			bestScore = bestFitness(population)
			log.write(str(evals) + "\t" + str(avgScore) + "\t" + str(bestScore) + "\n")


		log.write("\n")
	log.close()


if __name__ == "__main__":
	main()