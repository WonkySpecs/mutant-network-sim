import networkx as nx
import random

class Simulator():
	def __init__(self):
		print("Simulator instance created")
		print(self)
		self.graphStructure=None
		self.runSim(123)

	def loadGraphStructure(self, graph):
		self.graphStructure=graph

	def runSim(self, iterations):
		if self.graphStructure!=None:
			simGraph=self.graphStructure
			print(iterations)
		else:
			print("Failed to run sim: No graph loaded")