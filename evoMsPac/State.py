#Author: Michael Kammeyer

import random
import Ghost
import MsPac
import Pill

#Contains all board data including locations of all entities, dimensions of board, etc.
#Also tracks score, time, pills eaten, and "rank" for deciding moves.
class State(object):
	def __init__(self, width, height, ghosts, msPac, pDensity):
		self.height = height
		self.width = width
		self.pills = []
		self.ghosts = ghosts
		self.msPac = msPac
		self.time = 0
		self.totalTime = 0
		self.numEaten = 0
		self.totalPills = 0
		self.score = 0
		self.pDensity = pDensity
		self.distanceGhost = 0
		self.distancePill = 0
		self.rank = 0
		
	#Generates locations of all pills, ghosts, and msPac; resets scores and calculates distances
	def generateGrid(self, pDensity):
		self.time = self.width*self.height*2
		self.totalTime = self.time
		self.msPac.setDefaultLocation(self.height)
		self.pills = []
		self.score = 0
		self.numEaten = 0
		for ghost in self.ghosts:
			ghost.setDefaultLocation(self.width)

		for i in range(0, self.width):
			for j in range(0, self.height):
				if i != 0 or j != 0:
					rand = random.randrange(0, 100)
					if self.pDensity > rand:
						self.pills.append(Pill.Pill(i, j))

		self.totalPills = len(self.pills)

		for pill in self.pills:
			temp = abs(self.msPac.locationX - pill.x) + abs(self.msPac.locationY - pill.y)
			if temp > self.distancePill:
				self.distancePill = temp

		for ghost in self.ghosts:
			temp = abs(self.msPac.locationX - ghost.locationX) + abs(self.msPac.locationY - ghost.locationY)
			if temp > self.distanceGhost:
				self.distanceGhost = temp

	#Moves all entities for one move, recalculates values.
	def step(self, move):
		self.msPac.chooseStep(move)
		for ghost in self.ghosts:
			ghost.randomStep(self)

		for i in range(0, len(self.pills)):
			if self.pills[i].x == self.msPac.locationX:
				if self.pills[i].y == self.msPac.locationY:
					self.pills.pop(i)
					self.numEaten += 1
					break;

		for pill in self.pills:
			temp = abs(self.msPac.locationX - pill.x) + abs(self.msPac.locationY - pill.y)
			if temp > self.distancePill:
				self.distancePill = temp

		for ghost in self.ghosts:
			temp = abs(self.msPac.locationX - ghost.locationX) + abs(self.msPac.locationY - ghost.locationY)
			if temp > self.distanceGhost:
				self.distanceGhost = temp

		self.score = int((float(self.numEaten)/self.totalPills)*100)
		self.time-=1

	#Checks to see if game is over or not.
	def isGameOver(self):
		for ghost in self.ghosts:
			if self.msPac.locationX == ghost.locationX:
				if self.msPac.locationY == ghost.locationY:
					return True

		if len(self.pills) == 0:
			self.score += int((float(self.time)/self.totalTime)*100)
			return True

		if self.time == 0:
			return True

		return False

	#Evaluates the rank of current state using MsPac's controller
	def evaluateState(self):
		self.rank = self.evaluate(self.msPac.tree)

	def evaluate(self, tree):
		if tree.value == "DISTGHOST":
			return self.distanceGhost
		elif tree.value == "DISTPILL":
			return self.distancePill
		elif len(tree.children) == 1:
			return self.evaluate(tree.children[0])
		elif tree.value == "ADD":
			return self.evaluate(tree.children[0]) + self.evaluate(tree.children[1])
		elif tree.value == "SUB":
			return self.evaluate(tree.children[0]) - self.evaluate(tree.children[1])
		elif tree.value == "MULT":
			return self.evaluate(tree.children[0]) * self.evaluate(tree.children[1])
		elif tree.value == "DIV":
			temp = self.evaluate(tree.children[1])
			if temp == 0:
				temp = 1
			return self.evaluate(tree.children[0]) / temp
		elif tree.value == "RAND":
			temp = self.evaluate(tree.children[0])
			temp2 = self.evaluate(tree.children[1])

			if int(temp) == int(temp2):
				return temp
			elif temp > temp2:
				return random.randrange(int(temp2), int(temp))
			else:
				return random.randrange(int(temp), int(temp2))
		else:
			return tree.value