import random

class Ghost(object):
	def __init__(self):
		self.locationX = 0
		self.locationY = 0

	#Ghosts still only move randomly
	def randomStep(self, state):
		invalidMove = True
		while invalidMove:
			rand = random.randrange(0, 4)

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

	#resets ghost to starting spot on the board.
	def setDefaultLocation(self, width):
		self.locationX = width - 1
		self.locationY = 0