import random
import Node

class MsPac(object):
	def __init__(self):
		self.locationX = 0
		self.locationY = 0
		self.tree = 0
		self.functions = ["ADD", "SUB", "MULT", "DIV", "RAND"]
		self.terminals = ["DISTGHOST", "DISTPILL"]

	def getValidMoves(self, state):
		moves = ["STAY"]
		if self.locationX > 0:
			moves.append("LEFT")
		if self.locationY > 0:
			moves.append("UP")
		if self.locationX < state.width-1:
			moves.append("RIGHT")
		if self.locationY < state.height-1:
			moves.append("DOWN")

		return moves

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

	def chooseStep(self, move):
		if move == "LEFT":
			self.locationX-=1
		elif move == "UP":
			self.locationY-=1
		elif move == "RIGHT":
			self.locationX+=1
		elif move == "DOWN":
			self.locationY+=1

	def setDefaultLocation(self, height):
		self.locationY = height
		self.locationX = 0

	def generateGrowTree(self, maxDepth):
		self.tree = self.growNode(maxDepth)

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

	def generateFullTree(self, maxDepth):
		self.tree = self.fullNode(maxDepth)

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