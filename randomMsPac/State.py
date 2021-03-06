import random
import Ghost
import MsPac
import Pill

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

	def generateGrid(self, pDensity):
		self.time = self.width*self.height*2
		self.totalTime = self.time
		self.msPac.setDefaultLocation(self.height)
		for ghost in self.ghosts:
			ghost.setDefaultLocation(self.width)

		for i in range(0, self.width):
			for j in range(0, self.height):
				if i != 0 or j != 0:
					rand = random.randrange(0, 100)
					if self.pDensity > rand:
						self.pills.append(Pill.Pill(i, j))

		self.totalPills = len(self.pills)

	def step(self):
		self.msPac.randomStep(self)

		for ghost in self.ghosts:
			ghost.randomStep(self)

		for i in range(0, len(self.pills)):
			if self.pills[i].x == self.msPac.locationX:
				if self.pills[i].y == self.msPac.locationY:
					self.pills.pop(i)
					self.numEaten += 1
					break;

		self.score = int((float(self.numEaten)/self.totalPills)*100)
		self.time-=1

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

	def evaluate(self, tree):
		if tree.value == "DISTGHOST":
			return self.distanceGhost
		elif tree.value == "DISTPILL":
			return self.distancePill
		elif tree.value == "ADD":
			return evaluate(self, tree.children[0]) + evaluate(self, tree.children[1])
		elif tree.value == "SUB":
			return evaluate(self, tree.children[0]) - evaluate(self, tree.children[1])
		elif tree.value == "MULT":
			return evaluate(self, tree.children[0]) * evaluate(self, tree.children[1])
		elif tree.value == "DIV":
			return evaluate(self, tree.children[0]) / evaluate(self, tree.children[1])
		elif tree.value == "RAND":
			return random.randrange(evaluate(self, tree.children[0]), evaluate(self, tree.children[1]))