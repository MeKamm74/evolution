import random
import Ghost
import MsPac

class State:
	gridWidth
	gridHeight
	pills
	ghosts
	msPac

	def __init__(self):
		self.gridHeight = 0
		self.gridWidth = 0
		self.pills = []
		self.ghosts = []
		self.msPac = MsPac()

	def getGridHeight(self):
		return gridHeight

	def getGridWidth(self):
		return gridWidth

	def generateGrid(self, height, width, pDensity, seed):
		gridWidth = width
		gridHeight = height

		for i in range(0, width):
			for j in range(0, height):
				if pill:
					pills.append()