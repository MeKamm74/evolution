# Author: Michael Kammeyer
# This file will read in cnf data and generate random solutions for it. 
import re
import sys
import random
import datetime

f = open('1.cnf', 'r')

solution = []

firstLine = f.readline()

numVarsAndClauses = map(int, re.findall(r'\d+', firstLine))

current_time = datetime.datetime.now().time()

random.seed(current_time)

for i in range(0, numVarsAndClauses[0]):
    solution.append(bool(random.getrandbits(1)))

print solution

fitness = 0
neg = False

for line in f:
    currentLine = True
    words = line.split(' ')
    for word in words:
        num = int(word)
        if num < 0:
            num *= -1
            currentLine = not solution[num-1]
        elif num > 0:
            currentLine = solution[num-1]
        else:
            if currentLine == True:
                fitness+=1

print fitness

f.close()