import random

class MsPac:
	locationX
	locationY

	def __init__(self):
		self.locationX = 0
		self.locationY = 0

	def randomStep(self, state):
		invalidMove = True
		while invalidMove:
			rand = random.randRange(0, 5)

			if rand == 0:
				if self.locationX > 0:
					invalidMove = False
					self.locationX-=1
			elif rand == 1:
				if self.locationY > 0:
					invalidMove = False
					self.locationY-=1
			elif rand == 2:
				if self.locationX < state.gridWidth
					invalidMove = False
					self.locationX+=1
			elif rand == 3:
				if self.locationY < state.gridHeight
					invalidMove = False
					self.locationY+=1
			else:
				invalidMove = False