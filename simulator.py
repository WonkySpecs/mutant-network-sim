import networkx as nx
import random
import time

class Simulator():
	def __init__(self,graph=None):
		print("Simulator instance created")
		self.graphStructure=graph

	def loadGraphStructure(self, graph):
		self.graphStructure=graph
		if self.graphStructure==None:
			print("Warning: loadGraphStructure called with None as argument, current graph in Simulator is None")

	def runTrial(self,fitness,mStart=-1):
		sTime=time.time()
		simGraph=nx.DiGraph(self.graphStructure)
		numNodes=len(simGraph.node)
		if mStart==-1:
			mutantStart=random.randint(0,numNodes-1)
		else:
			mutantStart=mStart
		simGraph.node[mutantStart]['mutant']=True
		numMutants=1
		numNonMutants=numNodes-1
		iterations=0
		while numMutants!=0 and numNonMutants!=0:
			t=numMutants*fitness+numNonMutants
			nodeChoice=random.uniform(0,t)

			n=-1
			while nodeChoice>0:
				n+=1
				if simGraph.node[n]['mutant']==True:
					nodeChoice-=fitness
				else:
					nodeChoice-=1
			nodeReproducing=n

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
		print(str(iterations) + " iterations in " + str(time.time()-sTime))
		return iterations,numMutants,numNonMutants


	def runSim(self, trials,fitness=1.1):
		fixated=0
		extinct=0
		totalIter=0
		if self.graphStructure!=None:
			for i in range(trials):
				trial=self.runTrial(fitness)
				if i%(trials/10)==0:
					print(i)
				totalIter+=trial[0]
				if trial[1]==0:
					extinct+=1
				else:
					fixated+=1
			print(fixated,extinct,totalIter/trials)
			print(fixated/(extinct+fixated))
		else:
			print("Failed to run sim: No graph loaded")