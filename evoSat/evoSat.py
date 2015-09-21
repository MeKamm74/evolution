# Author: Michael Kammeyer
# Assignment 1b
import re
import sys
import random
import datetime
import time

# Each child has a solution and a calculated fitness
class Child:
    #default constructor, creates an empty child
    def __init__(self):
        self.solution = []
        self.fitness = 0

    #generates a random solution for the child
    def generateRandom(self, numVars):
        for i in range(numVars):
            self.solution.append(bool(random.getrandbits(1)))

    #evaluates the child's solution and stores it in the fitness attribute
    def evaluate(self, lines):
        for line in lines:
            words = line.split()

            if words[0] != 'c' and words[0] != 'p':
                currentLine = False

                for word in words:
                    num = int(word)
                    if num < 0:
                        num *= -1
                        currentLine = not self.solution[num-1]
                    elif num > 0:
                        currentLine = self.solution[num-1]
                    
                    if currentLine == True:
                        self.fitness+=1
                        break

#Takes a child as a parameter, returns a copy of that child.
def copy(child):
    newChild = Child()
    newChild.solution = child.solution
    newChild.fitness = child.fitness
    return newChild

#Returns the sum of all fitnesses in a list of children
def sumOfFitness(children):
    sum = 0
    for child in children:
        sum += child.fitness

    return sum

#Takes a list of children, Returns the index of the child with the highest fitness
def getFittest(children):
    best = 0
    index = 0
    for i in range(0, len(children)):
        if children[i].fitness > best:
            index = i
            best = children[i].fitness

    return index

#Takes a list of children, Returns the average of all their fitnesses
def getAverageFitness(children):
    total = 0
    for child in children:
        total += child.fitness
    avg = total/len(children)

    return avg
#Takes a list of children, Returns the index of the child with the lowest fitness
def getLeastFit(children):
    worst = children[0].fitness
    index = 0
    for i in range(1, len(children)):
        if children[i].fitness < worst:
            index = i

    return index

#uses either tournament or fitness proportional selection to return a list of children to use as parents
def getParents(children, k, lamda):
    if k:
        tournament = []
        for i in range(0, k):
            tournament.append(children[random.randrange(0, len(children))])

        parents = []
        for i in range(0, lamda):
            fittestIndex = getFittest(tournament)
            parents.append(tournament[fittestIndex])
            tournament.pop(fittestIndex)

        return parents

    else:
        parents = []
        totalFitness = sumOfFitness(children)
        for i in range(lamda):
            randomFitness = random.randrange(0, totalFitness)
            counter = 0
            for child in children:
                counter+=child.fitness
                if counter >= randomFitness:
                    parents.append(child)
                    break

        return parents

#creates new children from the list of parents using recombination, evaluates them and adds them to list of children
def createChildren(children, parents, lines):
    newChildren = []
    for i in range(0, len(parents)):
        child = Child()
        child.solution.extend(parents[i].solution[0:len(parents[i].solution)/2])
        child.solution.extend(parents[i*(-1)].solution[len(parents[i*(-1)].solution)/2:len(parents[i*(-1)].solution)])
        child.evaluate(lines)

        newChildren.append(child)

    children.extend(newChildren)
    return children

#uses either tournament or truncation for survival selection, removes children from the list
def cutLosers(children, k, lamda, toTruncate):
    if k:
        for i in range(0, lamda):
            indexes = random.sample(range(0, len(children)), k)
            tournament = []
            for j in indexes:
                tournament.append(children[j])
            leastFitIndex = getLeastFit(tournament)
            children.pop(indexes[leastFitIndex])

        return children

    else:
        children.sort(key=lambda x: x.fitness)
        toCut = population * toTruncate / 100
        for i in range(0, toCut):
            children.pop(i)
        while len(children) < population:
            for i in range(0, population-toCut):
                children.append(copy(children[i]))

        return children

#################################################################
# Main Script
# Reading in config file
if len(sys.argv) > 1:
    config = open(sys.argv[1], 'r')
else:
    config = open('default.cfg', 'r')

cnfFile = config.readline().split()[1]
seed = config.readline().split()[1]
runs = int(config.readline().split()[1])
logFile = config.readline().split()[1]
solFile = config.readline().split()[1]

config.readline()
config.readline()
config.readline()

population = int(config.readline().split()[1])
lamda = int(config.readline().split()[1])

config.readline()
config.readline()
config.readline()

parentTournament = config.readline().split()[1]
if parentTournament == 'True':
    k_parent = int(config.readline().split()[1])
else:
    k_parent = 0
    config.readline()

config.readline()
config.readline()
config.readline()

survivalTournament = config.readline().split()[1]
if survivalTournament == 'True':
    k_survival = int(config.readline().split()[1])
else:
    k_survival = 0
    config.readline()

toTruncate = int(config.readline().split()[1])

config.readline()
config.readline()
config.readline()

evals = int(config.readline().split()[1])
n = int(config.readline().split()[1])

f = open(cnfFile, 'r')
log = open(logFile, 'w')
sol = open(solFile, 'w')

#Seed random
current_time = time.mktime(datetime.datetime.now().timetuple())

if seed == "null":
    seed = current_time

random.seed(seed)

#Write log header
log.write("CNF File Name: ")
log.write(cnfFile)
log.write("\nRandom number seed value: ")
log.write(str(seed))
log.write("\nNumber of runs: ")
log.write(str(runs))
log.write("\nNumber of fitness evaluations per run: ")
log.write(str(evals))
log.write("\nPopulation size: " + str(population))
log.write("\nLambda: " + str(lamda))
log.write("\nK value for survival: " + str(k_survival))
log.write("\nK value for parents: " + str(k_parent))
log.write("\nN convergence number: " + str(n))
log.write("\n\nResults log\n\n")

#Store the cnf file
lines = []
for line in f:
    lines.append(line)

#Find the number of variables and clauses needed
for line in lines:
    if line[0] == 'p':
        words = line.split()
        numVars = int(words[2])
        numClauses = int(words[3])
        break

#Execute runs
for i in range(runs):
    log.write("Run: " + str(i) + "\n")
    children = []
    for j in range(population):
        child = Child()
        child.generateRandom(numVars)
        child.evaluate(lines)
        children.append(child)

    best = children[getFittest(children)].fitness
    bestSolution = children[getFittest(children)]
    avg = getAverageFitness(children)
    numEvals = population

    log.write(str(numEvals) + "\t")
    log.write(str(avg) + "\t")
    log.write(str(best) + "\n")

    bestTotalSolution = bestSolution
    terminate = False
    numAvg = 0
    numBest = 0
    prevAvg = 0
    prevBest = 0
    while(not terminate):
        parents = getParents(children, k_parent, lamda)
        children = createChildren(children, parents, lines)
        children = cutLosers(children, k_survival, lamda, toTruncate)

        numEvals+=lamda
        best = children[getFittest(children)].fitness
        bestSolution = children[getFittest(children)]
        avg = getAverageFitness(children)
        
        numAvg+=1
        if avg != prevAvg:
            prevAvg = avg
            numAvg = 0

        numBest+=1
        if best != prevBest:
            prevBest = best
            numBest = 0

        if numEvals >= evals:
            terminate = True
        if n:
            if numAvg >= n or numBest >= n:
                terminate = True

        log.write(str(numEvals) + "\t")
        log.write(str(avg) + "\t")
        log.write(str(best) + "\n")

    if bestSolution.fitness > bestTotalSolution.fitness:
        bestTotalSolution = bestSolution
    
    log.write("\n\n")

sol.write("c Solution for: ")
sol.write(cnfFile)
sol.write("\nc MAXSAT fitness value: ")
sol.write(str(bestTotalSolution.fitness))
sol.write("\nv ")

for i in range(0, len(bestTotalSolution.solution)):
    if bestTotalSolution.solution[i] == False:
        sol.write("-")
    sol.write(str(i+1))
    sol.write(" ")

config.close()  
log.close()
sol.close()
f.close()