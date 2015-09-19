# Author: Michael Kammeyer
# This file will read in cnf data and generate random solutions for it. 
import re
import sys
import random
import datetime
import time


class child:

    def __init__(self):
        numVarsAndClauses = map(int, re.findall(r'\d+', line))
        self.solution = []
        for i in range(0, numVarsAndClauses[0]):
            self.solution.append(bool(random.getrandbits(1)))

        self.fitness = 0

    def evaluate(self, lines):
        for line in lines:
            words = line.split(' ')

            if words[0] != 'c' && words[0] != p:
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
    for i in range(0, len(children)):
        if children[i].fitness > best:
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
        tournament.pop[fittestIndex]

    return winners

def createChildren(children, winners):
    


def cutLosers(children, k, lamda):
    tournament = []
    for i in range(0, k):
        tournament.append(children[random.randrange(0, len(children))])

    winners = []
    for i in range(0, lamda):
        fittestIndex = getFittest(tournament)
        winners.append(tournament[fittestIndex])
        tournament.pop[fittestIndex]

    children.extend(winners)


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

currentRun = 0
fitness = 0
highestTotalFitness = 0
for run in range(1, runs+1):
    currentEval = 0
    highestFitness = 0
    log.write("\nRun ")
    log.write(str(run))
    log.write("\n")
    while currentEval <= evals:
        currentEval+=1

        fitness = 0

        evaluate(lines)

        if fitness > highestFitness:
            log.write(str(currentEval))
            log.write("\t")
            log.write(str(fitness))
            log.write("\n")
            
            bestSolution = solution

            highestFitness = fitness

        if fitness == numVarsAndClauses[1]:
            break

    if highestFitness > highestTotalFitness:
        bestTotalSolution = bestSolution
        highestTotalFitness = highestFitness

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