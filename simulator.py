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

	def resetGraphStructure(self):
		if self.graphStructure==None:
			print("Tried to resetGraphStructure with no graph loaded, exiting")
			return -1
		else:
			g=self.graphStructure

			for i in range(len(g.node)):
				g.node[i]['mutant']=False
			return 1

	#Basic implementation for running moran process on the graph stored in self.graphStructure
	#Scales very poorly on graphs with a large number of ndoes as the algorithm can select 'useless' nodes to reproduce that will not change the state of the graph.
	def runTrial(self,fitness,mStart=-1):
		sTime=time.time()
		self.resetGraphStructure()
		simGraph=self.graphStructure#nx.Graph(self.graphStructure)
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

	#To enable simulation on large graphs, we must convert to a different (equivalent) algorithm.
	#This version only considers the 'useful' possibilities for selection of the reproducing node - this includes all mutant nodes and their direct neighbours.

	#MAY MERGE THIS WITH THE ORIGINAL AS AN OPTION, A LOT OF CODE REPLICATION HERE
	def runTrialV2(self,fitness,mStart=-1):
		sTime=time.time()
		#simGraph=nx.Graph(self.graphStructure)
		self.resetGraphStructure()
		simGraph=self.graphStructure
		print("creating graph took " + str(time.time()-sTime))
		numNodes=len(simGraph.node)
		if mStart==-1:
			mutantStart=random.randint(0,numNodes-1)
		else:
			mutantStart=mStart
		simGraph.node[mutantStart]['mutant']=True
		numMutants=1
		numNonMutants=numNodes-1
		iterations=0

		#The slight change to the method of selecting the node to reproduce (only from the active set) is the only real change from above, may want to merge together
		activeNodes=[i for i in simGraph.neighbors(mutantStart)]
		activeNodes.append(mutantStart)
		activeNonMutants=len(simGraph.neighbors(mutantStart))

		print("Set up for trial took " + str(time.time()-sTime))

		while numMutants!=0 and numNonMutants!=0:
			# print("ACTIVE NODES:" + str(activeNodes))
			# print('mutants: {}, nonmutants:{}, activeNonMutants{}\n'.format(numMutants,numNonMutants,activeNonMutants))

			if activeNonMutants+numMutants!=len(activeNodes):
				print("during simulation activeMutants+activeNonMutants was not equal to total number of active nodes: FIX THIS")
				#Handle this properly later
				sys.exit()
			t=(numMutants*fitness)+activeNonMutants
			nodeChoice=random.uniform(0,t)
			n=-1
			while nodeChoice>0:
				n+=1
				if simGraph.node[activeNodes[n]]['mutant']:
					nodeChoice-=fitness
				else:
					nodeChoice-=1
			nodeReproducing=activeNodes[n]

			possibleDyingNodes=simGraph.neighbors(nodeReproducing)

			if len(possibleDyingNodes)>0:
				nodeDying=possibleDyingNodes[random.randint(0,len(possibleDyingNodes)-1)]
			else:
				#Handle this properly at some point
				print("This graph contains an unconnected node, ceasing execution")
				sys.exit()

			#print(mutantStart,nodeReproducing,nodeDying)

			if simGraph.node[nodeReproducing]['mutant']!=simGraph.node[nodeDying]['mutant']:
				simGraph.node[nodeDying]['mutant']=simGraph.node[nodeReproducing]['mutant']
				if simGraph.node[nodeReproducing]['mutant']==True:
					#The new mutant must have been an activenonmutant before it died, so we add one to numMutants and subtract one from the other 2 numbers
					numMutants+=1
					numNonMutants-=1
					activeNonMutants-=1
					for n in simGraph.neighbors(nodeDying):
						if n not in activeNodes:
							activeNodes.append(n)
							activeNonMutants+=1
				else:
					numMutants-=1
					numNonMutants+=1
					activeNonMutants+=1

					#For each of the neighbours of the former mutant node, we check if any of their neighbours are now mutants- if not, remove from activeNodes
					#This process is technically O(n^2) but constants should be small, only possible problem could arise from highly connected graph (clique in particular, where this function is useless [all nodes are active] but will take lots of time)
					for i in simGraph.neighbors(nodeDying):
						if not simGraph.node[i]['mutant']:
							noLongerActive=True
							for j in simGraph.neighbors(i):
								if simGraph.node[j]['mutant']:
									noLongerActive=False
									break
							if noLongerActive:
								activeNodes.remove(i)
								activeNonMutants-=1

			iterations+=1
		print("Final mutants: {}, calculated {} iterations in {}s".format(numMutants,iterations,time.time()-sTime))
		return iterations,numMutants,numNonMutants

	def runSim(self, trials,fitness=1.1):
		fixated=0
		extinct=0
		totalIter=0
		if self.graphStructure!=None:
			for i in range(trials):
				trial=self.runTrialV2(fitness)
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