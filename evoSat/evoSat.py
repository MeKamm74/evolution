# Author: Michael Kammeyer
import re
import sys
import random
import datetime
import time

class Child:
    def __init__(self):
        self.solution = []
        self.fitness = 0

    def generateRandom(self, numVars):
        for i in range(numVars):
            self.solution.append(bool(random.getrandbits(1)))

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

def getFittest(children):
    best = 0
    index = 0
    for i in range(0, len(children)):
        if children[i].fitness > best:
            index = i

    return index

def getAverageFitness(children):
    total = 0
    for child in children:
        total += child.fitness
    avg = total/len(children)

    return avg

def getLeastFit(children):
    worst = children[0].fitness
    index = 0
    for i in range(1, len(children)):
        if children[i].fitness < worst:
            index = i

    return index

def getParents(children, k, lamda):
    tournament = []
    for i in range(0, k):
        tournament.append(children[random.randrange(0, len(children))])

    winners = []
    for i in range(0, lamda):
        fittestIndex = getFittest(tournament)
        winners.append(tournament[fittestIndex])
        tournament.pop(fittestIndex)

    return winners

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

def cutLosers(children, k, lamda):
    for i in range(0, lamda):
        indexes = random.sample(range(0, len(children)), k)
        tournament = []
        for j in indexes:
            tournament.append(children[j])
        leastFitIndex = getLeastFit(tournament)
        children.pop(indexes[leastFitIndex])

    return children


if len(sys.argv) > 1:
    config = open(sys.argv[1], 'r')
else:
    config = open('default.cfg', 'r')

cnfFile = config.readline().split()[1]
seed = config.readline().split()[1]
evals = int(config.readline().split()[1])
runs = int(config.readline().split()[1])
logFile = config.readline().split()[1]
solFile = config.readline().split()[1]
population = int(config.readline().split()[1])
lamda = int(config.readline().split()[1])
if(bool(config.readline().split()[1])):
    k = int(config.readline().split()[1])

f = open(cnfFile, 'r')
log = open(logFile, 'w')
sol = open(solFile, 'w')

current_time = time.mktime(datetime.datetime.now().timetuple())

if seed == "null":
    seed = current_time

random.seed(seed)

log.write("CNF File Name: ")
log.write(cnfFile)
log.write("\nRandom number seed value: ")
log.write(str(seed))
log.write("\nNumber of runs: ")
log.write(str(runs))
log.write("\nNumber of fitness evaluations per run: ")
log.write(str(evals))
log.write("\n\nResults log\n")

lines = []
for line in f:
    lines.append(line)

for line in lines:
    if line[0] == 'p':
        words = line.split()
        numVars = int(words[2])
        numClauses = int(words[3])
        break

bestTotalSolution = 0
for i in range(runs):
    children = []
    for j in range(population):
        child = Child()
        child.generateRandom(numVars)
        child.evaluate(lines)
        children.append(child)


    terminate = False
    evals = population
    while(not terminate):
        parents = getParents(children, k, lamda)
        children = createChildren(children, parents, lines)
        children = cutLosers(children, k, lamda)
        evals+=lamda
        best = getFittest(children)
        bestSolution = children[best].solution
        avg = getAverageFitness(children)
        if evals >= 10000:
            terminate = True
        print "EVALS: " + str(evals)
        print "AVG: " + str(avg)
        print "BEST: " + str(children[best].fitness)

sol.write("c Solution for: ")
sol.write(cnfFile)
sol.write("\nc MAXSAT fitness value: ")
sol.write(str(highestTotalFitness))
sol.write("\nv ")

for i in range(0, len(bestTotalSolution)):
    if bestTotalSolution[i] == False:
        sol.write("-")
    sol.write(str(i+1))
    sol.write(" ")

config.close()  
log.close()
sol.close()
f.close()