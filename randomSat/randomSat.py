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

cnfFile = config.readline().split(': ')[1]
seed = config.readline().split(': ')[1]
evals = config.readline().split(': ')[1]
runs = config.readline().split(': ')[1]
logFile = config.readline().split(': ')[1]
solFile = config.readline().split(': ')[1]

f = open(cnfFile, 'r')
log = open(logFile, 'w')
sol = open(solFile, 'w')

firstLine = f.readline()

numVarsAndClauses = map(int, re.findall(r'\d+', firstLine))

currentRun = 0
fitness = 0
current_time = time.mktime(datetime.datetime.now()).total_seconds
random.seed(current_time)

for run in range(1, runs):
    currentEval = 0
    while currnetEval <= evals:
        currentEval+=1

        fitness = 0
        f.seek(0)
        for line in f:
            words = line.split(' ')

            if words[0] == 'p':           
                numVarsAndClauses = map(int, re.findall(r'\d+', firstLine))
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

    f.close()