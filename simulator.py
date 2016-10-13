import networkx as nx
import random

class Simulator():
	def __init__(self,graph=None):
		print("Simulator instance created")
		print(self)
		self.graphStructure=graph

	def loadGraphStructure(self, graph):
		self.graphStructure=graph
		if self.graphStructure==None:
			print("Warning: loadGraphStructure called with None as argument, current graph in Simulator is None")

	def runSim(self, trials,fitness=1.1):
		if self.graphStructure!=None:
			for i in range(trials):
				#Reset graph to base state
				simGraph=nx.DiGraph(self.graphStructure)
				numNodes=len(simGraph.node)
				mutantStart=random.randint(0,numNodes-1)
				simGraph.node[mutantStart]['mutant']=True
				numMutants=1
				numNonMutants=numNodes-1
				iterations=0
				while numMutants!=0 and numNonMutants!=0:
					#Pick node at random, proportional to fitness
					#Pick random neighbour of node
					#If different, copy first node mutant status to second node

					#atm just selecting at random, change this to take fitness into account asap
					nodeReproducing=random.randint(0,numNodes-1)

					#If the reproducing node has at least one neighbour, choose one at random (uniform probability)
					if len(simGraph.neighbors(nodeReproducing))>0:
						nodeDying=random.sample(simGraph.neighbors(nodeReproducing),1)[0]
					
					if simGraph.node[nodeReproducing]['mutant']!=simGraph.node[nodeDying]['mutant']:
						simGraph.node[nodeDying]['mutant']=simGraph.node[nodeReproducing]['mutant']
						if simGraph.node[nodeReproducing]['mutant']==True:
							numMutants+=1
							numNonMutants-=1
						else:
							numMutants-=1
							numNonMutants+=1
					iterations+=1
				print(iterations,numMutants,numNonMutants)
		else:
			print("Failed to run sim: No graph loaded")