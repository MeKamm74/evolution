import random

class Node(object):
	def __init__(self, value):
		self.value = value
		self.children = []

	def addChild(self, value):
		self.children.append(Node(value))

	def popChild(self, x):
		self.children.pop(x)

	def combine(self, tree):
		if len(self.children) > 0:
			rand = random.randrange(0, len(self.children))
			return self.children[rand].combine(tree)

		else:
			nodes = tree.wholeTree()
			rand = random.randrange(0, len(nodes))
			self = nodes[rand]
		return self

	def mutate(self):

		if len(self.children) == 0:
			possibleValues = ["DISTGHOST", "DISTPILL"]
			rand = random.randrange(0, len(possibleValues))
			self.values = possibleValues[rand]
		else:
			rand = random.randrange(0, len(self.children))
			if rand == 0:
				possibleValues = ["DISTGHOST", "DISTPILL"]
				rand = random.randrange(0, len(possibleValues))
				self.values = possibleValues[rand]
			else:
				return self.children[rand].mutate()
		return self

	def wholeTree(self):
		tree = [self]
		for child in self.children:
			tree.extend(child.wholeTree())
		return tree