#Author: Michael Kammeyer

import random
import Node

class MsPac(object):
	def __init__(self):
		self.locationX = 0
		self.locationY = 0
		self.tree = 0
		#lists contain possible values in the tree
		self.functions = ["ADD", "SUB", "MULT", "DIV", "RAND"]
		self.terminals = ["DISTGHOST", "DISTPILL", "CONSTANT"]
		self.score = 0
		
	#Returns a list of valid moves
	def getValidMoves(self, state):
		moves = ["STAY"]
		occupied = False
		if self.locationX > 0:
			for ghost in state.ghosts:
				if ghost.locationX == self.locationX - 1 and ghost.locationY == self.locationY:
					occupied = True
			if not occupied:
				moves.append("LEFT")
			occupied = False
		if self.locationY > 0:
			for ghost in state.ghosts:
				if ghost.locationX == self.locationX and ghost.locationY == self.locationY-1:
					occupied = True
			if not occupied:
				moves.append("UP")
			occupied = False
		if self.locationX < state.width-1:
			for ghost in state.ghosts:
				if ghost.locationX == self.locationX + 1 and ghost.locationY == self.locationY:
					occupied = True
			if not occupied:
				moves.append("RIGHT")
			occupied = False
		if self.locationY < state.height-1:
			for ghost in state.ghosts:
				if ghost.locationX == self.locationX and ghost.locationY == self.locationY+1:
					occupied = True
			if not occupied:
				moves.append("DOWN")

		return moves

	#Makes a random valid move. Not used since evolving, but here if need be. 
	def randomStep(self, state):
		moves = getValidMoves(self, state)
		rand = random.randrange(0, len(moves))

		if moves[rand] == "LEFT":
			self.locationX-=1
		elif moves[rand] == "UP":
			self.locationY-=1
		elif moves[rand] == "RIGHT":
			self.locationX+=1
		elif moves[rand] == "DOWN":
			self.locationY+=1

	#Makes a given move.
	def chooseStep(self, move):
		if move == "LEFT":
			self.locationX-=1
		elif move == "UP":
			self.locationY-=1
		elif move == "RIGHT":
			self.locationX+=1
		elif move == "DOWN":
			self.locationY+=1

	#Resets msPac to starting location on board.
	def setDefaultLocation(self, height):
		self.locationY = height - 1
		self.locationX = 0

	#Generates a random grow tree
	def generateGrowTree(self, maxDepth):
		self.tree = self.growNode(maxDepth)

	#Recursive part from above.
	def growNode(self, maxDepth):
		if maxDepth > 1:

			rand = random.randrange(0, 2)

			if rand == 0:
				rand = random.randrange(0, len(self.functions))
				node = Node.Node(self.functions[rand])
				node.children.append(self.fullNode(maxDepth-1))
				node.children.append(self.fullNode(maxDepth-1))
		
			else:
				rand = random.randrange(0, len(self.terminals))
				node = Node.Node(self.terminals[rand])
		else:
			rand = random.randrange(0, len(self.terminals))
			node = Node.Node(self.terminals[rand])

		return node

	#Generates a random Full Tree
	def generateFullTree(self, maxDepth):
		self.tree = self.fullNode(maxDepth)

	#Recursive part from above.
	def fullNode(self, maxDepth):
		if maxDepth > 1:
			rand = random.randrange(0, len(self.functions))
			node = Node.Node(self.functions[rand])
			node.children.append(self.fullNode(maxDepth-1))
			node.children.append(self.fullNode(maxDepth-1))
		
		else:
			rand = random.randrange(0, len(self.terminals))
			node = Node.Node(self.terminals[rand])

		return node