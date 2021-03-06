import random

class MsPac(object):
	def __init__(self):
		self.locationX = 0
		self.locationY = 0
		self.tree = Node()

	def randomStep(self, state):
		invalidMove = True
		while invalidMove:
			rand = random.randrange(0, 5)

			if rand == 0:
				if self.locationX > 0:
					invalidMove = False
					self.locationX-=1
			elif rand == 1:
				if self.locationY > 0:
					invalidMove = False
					self.locationY-=1
			elif rand == 2:
				if self.locationX < state.width-1:
					invalidMove = False
					self.locationX+=1
			elif rand == 3:
				if self.locationY < state.height-1:
					invalidMove = False
					self.locationY+=1
			else:
				invalidMove = False

	def setDefaultLocation(self, height):
		self.locationY = height

	def evaluateState(self, state):
		eva
		if self.tree.data == "DISTGHOST":
			return state.distanceGhost
		elif self.tree.data == "DISTPILL":
			return state.distancePill

		elif self.tree.data == "ADD":
			return evaluate()
		self.tree