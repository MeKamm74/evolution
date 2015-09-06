# Author: Michael Kammeyer
# This file will read in cnf data and generate random solutions for it. 
import re
import sys
import random
import datetime
import time

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

currentRun = 0
fitness = 0
highestTotalFitness = 0
for run in range(1, runs+1):
    currentEval = 0
    highestFitness = 0
    f.seek(0)
    log.write("\nRun ")
    log.write(str(run))
    log.write("\n")
    while currentEval <= evals:
        currentEval+=1

        fitness = 0
        f.seek(0)
        for line in f:
            words = line.split(' ')

            if words[0] == 'p':           
                numVarsAndClauses = map(int, re.findall(r'\d+', line))
                solution = []
                for i in range(0, numVarsAndClauses[0]):
                    solution.append(bool(random.getrandbits(1)))
            
            elif words[0] != 'c':
                currentLine = False

                for word in words:
                    num = int(word)
                    if num < 0:
                        num *= -1
                        currentLine = not solution[num-1]
                    elif num > 0:
                        currentLine = solution[num-1]
                    
                    if currentLine == True:
                        fitness+=1
                        break

        print "Eval: ", currentEval
        print "Fitness: ", fitness

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