class Node(object):
	def __init__(self, value):
		self.value = value
		self.children = []

	def addChild(self, value):
		self.children.append(Node(value))

	def popChild(self, x):
		self.children.pop(x)

	