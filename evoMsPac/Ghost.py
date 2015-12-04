import random
import Node

class Ghost(object):
	def __init__(self):
		self.locationX = 0
		self.locationY = 0
		self.tree = 0
		#lists contain possible values in the tree
		self.functions = ["ADD", "SUB", "MULT", "DIV", "RAND"]
		self.terminals = ["DISTGHOST", "DISTPAC", "CONSTANT"]
		self.distanceGhost = 0
		self.distancePac = 0
		self.score = 0

	#resets ghost to starting spot on the board.
	def setDefaultLocation(self, width):
		self.locationX = width - 1
		self.locationY = 0

		#Returns a list of valid moves
	def getValidMoves(self, state):
		moves = []
		if self.locationX > 0:
			moves.append("LEFT")
		if self.locationY > 0:
			moves.append("UP")
		if self.locationX < state.width-1:
			moves.append("RIGHT")
		if self.locationY < state.height-1:
			moves.append("DOWN")

		return moves

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