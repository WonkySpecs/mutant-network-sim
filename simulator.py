import networkx as nx
import random

class Simulator():
	def __init__(self,graph=None):
		print("Simulator instance created")
		print(self)
		self.graphStructure=graph
		self.runSim(123)

	def loadGraphStructure(self, graph):
		self.graphStructure=graph

	def runSim(self, iterations):
		if self.graphStructure!=None:

			for i in range(iterations):
				#Reset graph to base state
				simGraph=self.graphStructure
				mutantStart=random.randint(0,len(simGraph.node)-1)
				simGraph.node[mutantStart]['mutant']=True

			print(iterations)
		else:
			print("Failed to run sim: No graph loaded")