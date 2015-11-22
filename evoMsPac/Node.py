#Author: Michael Kammeyer

import random

class Node(object):
	#Constructer, sets value. Generates random constant if applicable.
	def __init__(self, value):
		if value == "CONSTANT":
			self.value = random.randint(0, 10) + random.random()
		else:
			self.value = value
		self.children = []

	def addChild(self, value):
		self.children.append(Node(value))

	def popChild(self, x):
		self.children.pop(x)

	#sets a random node in tree rooted at current node equal to a random node in second tree
	def combine(self, tree):
		rand = random.randrange(0, 2)
		if len(self.children) > 0 and rand == 0:
			rand = random.randrange(0, len(self.children))
			return self.children[rand].combine(tree)

		else:
			nodes = tree.wholeTree()
			rand = random.randrange(0, len(nodes))
			self = nodes[rand]
		return self

	#Mutates one node in the tree rooted at the current node
	def mutate(self):

		if len(self.children) == 0:
			possibleValues = ["DISTGHOST", "DISTPILL", "CONSTANT"]
			rand = random.randrange(0, len(possibleValues))
			if possibleValues[rand] == "CONSTANT":
				self.values = random.randint(0, 10) + random.random()
			else:
				self.values = possibleValues[rand]
		else:
			rand = random.randrange(0, len(self.children))
			if rand == 0:
				possibleValues = ["DISTGHOST", "DISTPILL", "CONSTANT"]
				rand = random.randrange(0, len(possibleValues))
				if possibleValues[rand] == "CONSTANT":
					self.values = random.randint(0, 10) + random.random()
				else:
					self.values = possibleValues[rand]
			else:
				return self.children[rand].mutate()
		return self

	#Returns a list that contains every node in the tree rooted at current node
	def wholeTree(self):
		tree = [self]
		for child in self.children:
			tree.extend(child.wholeTree())
		return tree

	#Returns a string representation of tree rooted at current node 
	def printOut(self, num):
		output = str(self.value) + "\n"
		for child in self.children:
			for i in range(0, num):
				output += "\t"
			output += child.printOut(num+1)

		return output