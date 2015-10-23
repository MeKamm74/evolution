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
        self.correctClauses = 0
        self.valuesNotUsed = 0
        self.fitness = 0

    #generates a random solution for the child
    def generateRandom(self, numVars):
        for i in range(numVars):
            rand = random.randrange(0, 3);
            if rand == 0:
                self.solution.append('F')
            elif rand == 1:
                self.solution.append('T')
            else:
                self.solution.append('X')

    #evaluates the child's solution and stores it in the numClauses attribute
    def evaluateCorrectClauses(self, lines):
        for line in lines:
            words = line.split()

            if words[0] != 'c' and words[0] != 'p':
                currentLine = False

                for word in words:
                    num = int(word)

                    if num < 0:
                        num *= -1
                        if self.solution == 'F'
                            currentLine = True
                    
                    elif num > 0:
                        if self.solution == 'T'
                            currentLine = True
                    
                    if currentLine == True:
                        self.correctClauses+=1
                        break

    def evaluteDontCares(self):
        count = 0
        for value in self.solution:
            if value == 'X':
                count++

        return count

    def dominates(self, child):
        dominates = False
        if self.correctClauses >= child.correctClauses and self.valuesNotUsed >= child.valuesNotUsed:
            if self.correctClauses > child.correctClauses or self.valuesNotUsed > child.valuesNotUsed:
                dominates = True

        return dominates

def paretoSortChildren(children):
    frontTable = []

    for child in children:
        frontTable = paretoSortChild(child, frontTable)

    children = []

    for front in frontTable:
        for child in front:
            children.append(child)

    return child

def paretoSortChild(child, frontTable):
    if len(frontTable) == 0:
        frontTable.append([])

    for j in range(0, len(frontTable)):
        if len(frontTable[j]) == 0:
            frontTable[j].append(child)
            break

        for i in range(0, len(front)):
            if frontTable[j][i].dominates(child):
                break
            elif child.dominates(frontTable[j][i]):
                frontTable[j].pop(i)
                frontTable[j].append(child)
                frontTable = paretoSortChild(child, frontTable)
                done = True
            else:
                frontTable[j].append(child)
                done = True

        if done = True:
            break
        elif j == len(frontTable) - 1:
            frontTable.append([])

    return frontTable 

def generateSeed(seedFile, children, numVars):
    seed = open(seedFile, 'r')
    for line in seed:
        words = line.split()
        chaild = Child()
        for word in words:
            if int(word) > 0:
                child.solution.append(True)
            else:
                child.solution.append(False)
        child.evaluateCorrectClauses(lines)
        child.evaluteDontCares()
        children.append(child)

    for i in range(population - len(children)):
        child = Child()
        child.generateRandom(numVars)
        children.append(child)

    return children

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

def inverseSumOfFitness(children):
    sum = 0
    for child in children:
        sum += 1/float(child.fitness)

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
    avg = float(total)/len(children)

    if adapt == "True":
        mutationRate = 100*(avg/numClauses)
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
    parents = []
    if randomParent == "True":
        for i in range(0, lamda):
            parents.append(children[random.randrange(0, len(children))])
            
    elif parentTournament == "True":
        for j in range(0, lamda):  
            tournament = []
            for i in range(0, k):
                tournament.append(children[random.randrange(0, len(children))])

            fittestIndex = getFittest(tournament)
            parents.append(tournament[fittestIndex])

    else:
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
        crossoverPoint = random.randrange(0, len(parents[i].solution))
        child.solution.extend(parents[i].solution[0:crossoverPoint])
        child.solution.extend(parents[i*(-1)].solution[crossoverPoint:len(parents[i*(-1)].solution)])
        child = mutate(child)
        child.evaluateCorrectClauses(lines)
        child.evaluteDontCares()
        newChildren.append(child)

    if commaOrPlus == 'comma':
        children = newChildren

    else:
        children.extend(newChildren)

    children = paretoSortChildren(children)
    return children

def mutate(child):
    rand = random.randrange(0, 100)
    if rand > mutationRate:
        randChild = random.randrange(0, len(child.solution))
        rand = random.randrange(0, 2)
        if child.solution[randChild] == 'T':
            if rand == 0:
                child.solution[randChild] == 'F'
            else:
                child.solution[randChild] == 'X'
        elif child.solution[randChild] == 'F':
            if rand == 0:
                child.solution[randChild] == 'T'
            else:
                child.solution[randChild] == 'X'
        else:
            if rand == 0:
                child.solution[randChild] == 'F'
            else:
                child.solution[randChild] == 'T'
    return child

#uses either tournament or truncation for survival selection, removes children from the list
def cutLosers(children, k, lamda):
    if randomSurvival == "True":
        if commaOrPlus == "comma":
            for i in range(lamda - population):
                children.pop(random.randrange(0, len(children)))    
        else:
            for i in range(population - lamda):
                children.pop(random.randrange(0, len(children)))

    elif survivalTournament == "True":
        for i in range(0, lamda):
            indexes = random.sample(range(0, len(children)), k)
            tournament = []
            for j in indexes:
                tournament.append(children[j])
            leastFitIndex = getLeastFit(tournament)
            children.pop(indexes[leastFitIndex])

        return children

    elif fitnessSurvival == "True":
        totalFitness = inverseSumOfFitness(children)
        for i in range(lamda):
            randomFitness = random.randrange(0, totalFitness)
            counter = 0
            for child in children:
                counter+=1/float(child.fitness)
                if counter >= randomFitness:
                    parents.append(child)
                    break
    else:
        children.sort(key=lambda x: x.fitness)
        while len(children) > population:
            children.pop(0)

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
seedFile = config.readline().split()[1]

config.readline()
config.readline()
config.readline()

population = int(config.readline().split()[1])
lamda = int(config.readline().split()[1])

config.readline()
config.readline()
config.readline()

commaOrPlus = config.readline().split()[1]
adapt = config.readline().split()[1]

config.readline()
config.readline()
config.readline()

parentTournament = config.readline().split()[1]
if parentTournament == 'True':
    k_parent = int(config.readline().split()[1])
else:
    k_parent = 0
    config.readline()

fitnessParent = config.readline().split()[1]
randomParent = config.readline().split()[1]

config.readline()
config.readline()
config.readline()

survivalTournament = config.readline().split()[1]
if survivalTournament == 'True':
    k_survival = int(config.readline().split()[1])
else:
    k_survival = 0
    config.readline()

truncate = config.readline().split()[1]
randomSurvival = config.readline().split()[1]
fitnessSurvival = config.readline().split()[1]
config.readline()
config.readline()
config.readline()

restart = config.readline().split()[1]
r = int(config.readline().split()[1]) 
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
log.write("\nStrategy: " + commaOrPlus)
log.write("\nSelf-Adaptivity: " + str(adapt))
log.write("\nRestarts: " + str(restart))
log.write("\nR-Elitism: " + str(r))

if parentTournament == "True":
    log.write("\nParent Selection: Tournament")
elif randomParent == "True":
    log.write("\nParent Selection: Random")
elif fitnessParent == "True":
    log.write("\nParent Selection: Fitness proportional")

if survivalTournament == "True":
    log.write("\nSurvival Selection: Tournament")
elif randomSurvival == "True":
    log.write("\nSurvival Selection: Random")
elif fitnessSurvival == "True":
    log.write("\nSurvival Selection: Fitness proportional")
elif truncate == "True":
    log.write("\nSurvival Selection: Truncation")

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

mutationRate = 99
bestTotalSolution = Child()
#Execute runs
for i in range(runs):
    log.write("Run " + str(i + 1) + "\n")
    children = []

    if seedFile != "none":
        generateSeed(seedFile, children, numVars)

    else:    
        for j in range(population):
            child = Child()
            child.generateRandom(numVars)
            child.evaluateCorrectClauses(lines)
            child.evaluteDontCares()
            children.append(child)

    best = children[getFittest(children)].fitness
    bestSolution = children[getFittest(children)]
    avg = getAverageFitness(children)
    numEvals = population

    log.write(str(numEvals) + "\t")
    log.write(str(avg) + "\t")
    log.write(str(best) + "\n")

    terminate = False
    reset = False
    numAvg = 0
    numBest = 0
    prevAvg = 0
    prevBest = 0
    while(not terminate):
        if reset:
            for j in range(population - r):
                children.pop(getLeastFit(children))

            reset = False
            numAvg = 0
            numBest = 0
            prevAvg = 0
            prevBest = 0
            children = []
            for j in range(population - r):
                child = Child()
                child.generateRandom(numVars)
                child.evaluateCorrectClauses(lines)
                child.evaluteDontCares()
                children.append(child)

        parents = getParents(children, k_parent, lamda)
        children = createChildren(children, parents, lines)
        children = cutLosers(children, k_survival, lamda)

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
        if restart:
            if numAvg >= n or numBest >= n:
                reset = True

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