#Author: Michael Kammeyer

import sys
import Ghost
import MsPac
import State
import time
import datetime
import random
#Returns the move for Ms. Pacman to make
def chooseMove(moves, state, numGhost=-1):
	if numGhost == -1:
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

	else:
		bestRank = -9999999
		best = ""
		for move in moves:
			if move == "LEFT":
				tempState = state
				tempState.ghosts[numGhost].locationX -= 1
				tempState.evaluateGhostState(numGhost)
				if tempState.rank > bestRank:
					best = move
					bestRank = tempState.rank
			if move == "RIGHT":
				tempState = state
				tempState.ghosts[numGhost].locationX += 1
				tempState.evaluateGhostState(numGhost)
				if tempState.rank > bestRank:
					best = move
					bestRank = tempState.rank
			if move == "UP":
				tempState = state
				tempState.ghosts[numGhost].locationY -= 1
				tempState.evaluateGhostState(numGhost)
				if tempState.rank > bestRank:
					best = move
					bestRank = tempState.rank
			if move == "DOWN":
				tempState = state
				tempState.ghosts[numGhost].locationY += 1
				tempState.evaluateGhostState(numGhost)
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
		pacMoves = state.msPac.getValidMoves(state)
		move = chooseMove(pacMoves, state)

		ghostMoves = []
		for i in range(0, len(state.ghosts)):
			moves = state.ghosts[i].getValidMoves(state)
			ghostMoves.append(chooseMove(moves, state, i))
		#Update the board
		state.step(move, ghostMoves)

		#World Log
		tempWorld += "m" + " " + str(state.msPac.locationX) + " " + str(state.msPac.locationY) + "\n"
		for k in range(0, len(state.ghosts)):
			tempWorld += str(k+1) + " " + str(state.ghosts[k].locationX) + " " + str(state.ghosts[k].locationY) + "\n"
		tempWorld += "t" + " " + str(state.time) + " " + str(state.score) + "\n"
		
		#Check if game is over
		gameOver = state.isGameOver()

	return state, tempWorld

#Chooses Parents, combines or mutates them to create children, evaluates them, and adds them to the population
def createChildren(populationMsPac, populationGhosts, genSize, bestOverallScore, worldFile, solFile, pDensity, maxDepth, p, parentSelection, width, height):
	children = []
	i = 0
	while i < genSize:
		#Choose Parents
		rand = random.randrange(0, 2)
		if rand == 0:
			msPacParents = chooseParents(populationMsPac, parentSelection, 2)
			tree1, tree2 = combine(msPacParents)

			msPac1 = MsPac.MsPac()
			msPac1.tree = tree1
			msPac2 = MsPac.MsPac()
			msPac2.tree = tree2

			ghostParents = chooseParents(populationGhosts, parentSelection, 2)
			tree1, tree2 = combine(ghostParents)

			ghost1 = Ghost.Ghost()
			ghost1.tree = tree1
			ghost2 = Ghost.Ghost()
			ghost2.tree = tree2

			ghosts1 = [ghost1]
			ghosts2 = [ghost2]

			for j in range(1, 3):
				ghost = Ghost.Ghost()
				ghost.tree = ghosts1[0].tree
				ghosts1.append(ghost)

				newGhost = Ghost.Ghost()
				newGhost.tree = ghosts2[0].tree
				ghosts2.append(newGhost)

			child1 = State.State(width, height, ghosts1, msPac1, pDensity)
			child2 = State.State(width, height, ghosts2, msPac2, pDensity)

			child1.generateGrid(pDensity)
			child1, tempWorld1 = runGame(child1)
			child1 = penalty(child1, p, maxDepth)
			child2.generateGrid(pDensity)
			child2, tempWorld2 = runGame(child2)
			child2 = penalty(child2, p, maxDepth)

			child1.ghosts[0].score = child1.score * -1
			child1.msPac.score = child1.score
			populationGhosts.append(child1.ghosts[0])
			populationMsPac.append(child1.msPac)

			child2.ghosts[0].score = child2.score * -1
			child2.msPac.score = child2.score
			populationGhosts.append(child2.ghosts[0])
			populationMsPac.append(child2.msPac)
			if child1.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = child1.score
				world = open(worldFile, 'w')
				world.write(tempWorld1)
				world.close() 

				solution = open(solFile, 'w')
				solution.write(child1.msPac.tree.printOut(1))
				solution.write("\n\n")
				solution.write(child1.ghosts[0].tree.printOut(1))
				solution.close()

			if child2.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = child2.score
				world = open(worldFile, 'w')
				world.write(tempWorld2)
				world.close() 

				solution = open(solFile, 'w')
				solution.write(child2.msPac.tree.printOut(1))
				solution.write("\n\n")
				solution.write(child2.ghosts[0].tree.printOut(1))
				solution.close()

			i+=2

		else:
			parentsMsPac = chooseParents(populationMsPac, parentSelection, 1)
			parentsGhosts = chooseParents(populationGhosts, parentSelection, 1)
			tree = parentsMsPac[0].tree
			msPac = MsPac.MsPac()
			msPac.tree = tree
			msPac = mutate(msPac)

			tree = parentsGhosts[0].tree
			ghost = Ghost.Ghost()
			ghost.tree = tree
			ghost = mutate(ghost)
			ghosts = [ghost]

			for j in range(1, 3):
				newGhost = Ghost.Ghost()
				newGhost.tree = ghosts[0].tree
				ghosts.append(newGhost)

			child = State.State(width, height, ghosts, msPac, pDensity)
			child.generateGrid(pDensity)
			child, tempWorld = runGame(child)
			child = penalty(child, p, maxDepth)
			
			child.ghosts[0].score = child.score * -1
			child.msPac.score = child.score
			populationGhosts.append(child.ghosts[0])
			populationMsPac.append(child.msPac)

			if child.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = child.score
				world = open(worldFile, 'w')
				world.write(tempWorld)
				world.close() 

				solution = open(solFile, 'w')
				solution.write(child.msPac.tree.printOut(1))
				solution.write("\n\n")
				solution.write(child.ghosts[0].tree.printOut(1))
				solution.close()

			i+=1

	return populationMsPac, populationGhosts, bestOverallScore

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
			totalTop = totalFitness(s1)
			totalBottom = totalFitness(s2)
			count = 0
			rand = random.randrange(1, 101)
			if rand < 80 and len(s1) > 0:
				if totalTop > 0:
					rand = random.randrange(0, totalTop)
					for i in range(0, len(s1)):
						count += s1[i].score
						if count > rand:
							parents.append(s1.pop(i))
							break

				elif totalTop == 0:
					rand = random.randrange(0, len(s1))
					parents.append(s1.pop(rand))
					break

				else:
					rand = random.randrange(0, abs(totalTop))
					for i in range(0, len(s1)):
						count += abs(s1[i].score)
						if count > rand:
							parents.append(s1.pop(i))
							break
			else:
				if totalBottom >= 0:
					rand = random.randrange(0, totalBottom)
					for i in range(0, len(s2)):
						count += s2[i].score
						if count > rand:
							parents.append(s2.pop(i))
							break

				elif totalBottom == 0:
					rand = random.randrange(0, len(s2))
					parents.append(s2.pop(rand))
					break

				else:
					rand = random.randrange(0, abs(totalBottom))
					for i in range(0, len(s2)):
						count += abs(s2[i].score)
						if count > rand:
							parents.append(s2.pop(i))
							break

	else:
		for i in range(0, num):
			total = totalFitness(population)
			count = 0
			if total == 0:
				rand = random.randrange(0, len(population))
				parents.append(population[rand])
			elif total < 0:
				rand = random.randrange(0, abs(total))
				for state in population:
					count += abs(state.score)
					if count > rand:
						parents.append(state)
						break
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
	tree1 = parents[0].tree
	tree2 = parents[1].tree
	tree1.combine(parents[1].tree)
	tree2.combine(parents[0].tree)

	return tree1, tree2

#returns a mutation of one parent.
def mutate(child):
	child.tree.mutate()
	return child

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

#Main Script
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
		populationGhosts = []
		populationMsPac = []
		for j in range(0, popSize/2):
			msPac = MsPac.MsPac()
			msPac.generateFullTree(maxDepth)
			populationMsPac.append(msPac)

			ghost = Ghost.Ghost()
			ghost.generateFullTree(maxDepth)
			ghosts = [ghost]
			for i in range(1, 3):
				newGhost = Ghost.Ghost()
				newGhost.tree = ghosts[0].tree
				ghosts.append(newGhost)

			state = State.State(width, height, ghosts, msPac, pDensity)
			state.generateGrid(pDensity)

			state, tempWorld = runGame(state)
			state.msPac.score = state.score
			state.ghosts[0].score = state.score * -1

			populationMsPac.append(state.msPac)
			populationGhosts.append(state.ghosts[0])

			if state.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = state.score
				world = open(worldFile, 'w')
				world.write(tempWorld)
				world.close() 

				solution = open(solFile, 'w')
				solution.write(state.msPac.tree.printOut(1))
				solution.write("\n\n")
				solution.write(state.ghosts[0].tree.printOut(1))
				solution.close()

		#Then Grow trees
		for j in range(popSize/2, popSize):
			msPac = MsPac.MsPac()
			msPac.generateGrowTree(maxDepth)
			populationMsPac.append(msPac)
			
			ghost = Ghost.Ghost()
			ghost.generateGrowTree(maxDepth)
			ghosts = [ghost]
			for i in range(1, 3):
				newGhost = Ghost.Ghost()
				newGhost.tree = ghosts[0].tree
				ghosts.append(newGhost)

			state = State.State(width, height, ghosts, msPac, pDensity)
			state.generateGrid(pDensity)

			state, tempWorld = runGame(state)
			state.msPac.score = state.score
			state.ghosts[0].score = state.score * -1

			populationMsPac.append(state.msPac)
			populationGhosts.append(state.ghosts[0])

			if state.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = state.score
				world = open(worldFile, 'w')
				world.write(tempWorld)
				world.close() 

				solution = open(solFile, 'w')
				solution.write(state.msPac.tree.printOut(1))
				solution.write("\n\n")
				solution.write(state.ghosts[0].tree.printOut(1))
				solution.close()

		#Calculates bests and averages for initial population
		evals += len(populationMsPac)
		avgScore = averageFitness(populationMsPac)
		bestScore = bestFitness(populationMsPac)
		log.write(str(evals) + "\t" + str(avgScore) + "\t" + str(bestScore) + "\n")	
		terminate = False
		previousBest = bestScore
		tillConverge = n

		#Runs a generation while termination criteria is not met.
		while not terminate:
			#Create Children
			populationMsPac, populationGhosts, bestOverallScore = createChildren(populationMsPac, populationGhosts, genSize, bestOverallScore, worldFile, solFile, pDensity, maxDepth, p, parentSelection, width, height)
			
			#Survival Selection
			populationMsPac = cutLosers(populationMsPac, popSize, k)
			populationGhosts = cutLosers(populationGhosts, popSize, k)
			#Update number of evals
			evals += genSize

			#Log
			avgScore = averageFitness(populationMsPac)
			bestScore = bestFitness(populationMsPac)
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