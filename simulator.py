import networkx as nx
import random
import time
import sys


class Simulator():
	def __init__(self, printOutput = True, graph = None):
		print("Simulator instance created")
		self.graphStructure = graph
		self.printingOutput = printOutput

	def loadGraphStructure(self, graph):
		self.graphStructure = graph
		if self.graphStructure == None:
			print("Warning: loadGraphStructure called with None as argument, current graph in Simulator is None")

	#At the moment, just sets 'mutant' to False for all nodes. Can extend in the future
	def resetGraphStructure(self):
		if self.graphStructure == None:
			print("Tried to resetGraphStructure with no graph loaded, exiting")
			return -1
		else:
			g = self.graphStructure

			for i in range(len(g.node)):
				g.node[i]['mutant'] = False
			return 1

	#Basic implementation for running moran process on the graph stored in self.graphStructure
	#Scales very poorly on graphs with a large number of ndoes as the algorithm often select 'useless' nodes to reproduce that will not change the state of the graph.
	def runTrial(self, fitness, mStart = -1):
		#Initialization
		sTime = time.time()
		self.resetGraphStructure()
		simGraph = self.graphStructure #nx.Graph(self.graphStructure)
		numNodes = len(simGraph.node)
		if mStart == -1:
			mutantStart = random.randint(0, numNodes-1)
		else:
			mutantStart = mStart
		simGraph.node[mutantStart]['mutant']=True
		numMutants = 1
		numNonMutants = numNodes-1
		iterations = 0

		#Until mutant has fixated or gone extinct, choose a node, choose a neighbour and reproduce
		while numMutants!=0 and numNonMutants!=0:
			t = numMutants*fitness+numNonMutants
			nodeChoice = random.uniform(0, t)

			n = -1
			while nodeChoice>0:
				n += 1
				if simGraph.node[n]['mutant']==True:
					nodeChoice -= fitness
				else:
					nodeChoice -= 1
			nodeReproducing = n

			#If the reproducing node has at least one neighbour, choose one at random (uniform probability)
			if len(simGraph.neighbors(nodeReproducing))>0:
				nodeDying = random.sample(simGraph.neighbors(nodeReproducing), 1)[0]
			
			if simGraph.node[nodeReproducing]['mutant']!=simGraph.node[nodeDying]['mutant']:
				simGraph.node[nodeDying]['mutant']=simGraph.node[nodeReproducing]['mutant']
				if simGraph.node[nodeReproducing]['mutant']==True:
					numMutants += 1
					numNonMutants -= 1
				else:
					numMutants -= 1
					numNonMutants += 1
			iterations += 1
		if self.printingOutput:
			print("Final mutants: {}, calculated {} iterations in {}s".format(numMutants, iterations, time.time()-sTime))
		return iterations, numMutants, numNonMutants

	#To enable simulation on large graphs, we must convert to a different (equivalent) algorithm.
	#This version only considers the 'useful' possibilities for selection of the reproducing node - this includes all mutant nodes and their direct neighbours.

	#MAY MERGE THIS WITH THE ORIGINAL AS AN OPTION, A LOT OF CODE REPLICATION HERE
	def runTrialV2(self, fitness, mStart = -1):
		#Initialization
		sTime = time.time()
		self.resetGraphStructure()
		simGraph = self.graphStructure #nx.Graph(self.graphStructure)
		numNodes = len(simGraph.node)
		if mStart == -1:
			mutantStart = random.randint(0, numNodes-1)
		else:
			mutantStart = mStart
		simGraph.node[mutantStart]['mutant'] = True
		numMutants = 1
		numNonMutants = numNodes-1
		iterations = 0

		#The slight change to the method of selecting the node to reproduce (only from the active set) is the only real change from above, may want to merge together
		activeMutants = [mutantStart]
		activeNonMutants = [i for i in simGraph.neighbors(mutantStart)]

		while numMutants!=0 and numNonMutants!=0:
			#c is total fitness of active ndoes
			c = random.uniform(0, (len(activeMutants)*fitness)+len(activeNonMutants))

			#Each mmutant/non-mutant is as likely as any other, so we just pick one set or the other then pick at random from that set
			if c > len(activeNonMutants):
				nodeReproducing = activeMutants[random.randint(0, len(activeMutants) - 1)]
			else:
				nodeReproducing = activeNonMutants[random.randint(0, len(activeNonMutants) - 1)]

			possibleDyingNodes = simGraph.neighbors(nodeReproducing)

			if len(possibleDyingNodes)>0:
				nodeDying = possibleDyingNodes[random.randint(0, len(possibleDyingNodes)-1)]
			else:
				#Handle this properly at some point
				print("This graph contains an unconnected node, ceasing execution")
				sys.exit()

			if simGraph.node[nodeReproducing]['mutant']!=simGraph.node[nodeDying]['mutant']:
				simGraph.node[nodeDying]['mutant']=simGraph.node[nodeReproducing]['mutant']
				if simGraph.node[nodeReproducing]['mutant']==True:
					#The new mutant must have been an activenonmutant before it died, so we move it from activeNonMutants to activeMutants
					numMutants += 1
					numNonMutants -= 1
					activeNonMutants.remove(nodeDying)

					#Check if new mutant has any non mutant neighbours - if so, isActive is true, otherwise not
					isActive = False
					for n in simGraph.neighbors(nodeDying):
						#If any non mutant neighbours of the new mutant were not active, they are now
						if not simGraph.node[n]['mutant']:
							isActive = True
							if n not in activeNonMutants:
								activeNonMutants.append(n)
						#If any mutant neighbour of the new mutant no longer has any non mutant neighbours it is no longer active
						else:
							stillActive = False
							for nn in simGraph.neighbors(n):
								if not simGraph.node[nn]['mutant']:
									stillActive = True
									break
							if not stillActive:
								activeMutants.remove(n)
					if isActive:
						activeMutants.append(nodeDying)
				else:
					numMutants -= 1
					numNonMutants += 1

					activeMutants.remove(nodeDying)
					activeNonMutants.append(nodeDying)

					for i in simGraph.neighbors(nodeDying):
						if not simGraph.node[i]['mutant']:
							noLongerActive = True
							for j in simGraph.neighbors(i):
								if simGraph.node[j]['mutant']:
									noLongerActive = False
									break
							if noLongerActive:
								activeNonMutants.remove(i)
						else:
							if i not in activeMutants:
								activeMutants.append(i)

			iterations += 1
		if self.printingOutput:
			print("Final mutants: {}, calculated {} iterations in {}s".format(numMutants, iterations, time.time()-sTime))
		return iterations, numMutants, numNonMutants


	def runSim(self, trials, fitness = 1.1, mStart = -1):
		fixated = 0
		extinct = 0
		totalIter = 0
		if self.graphStructure!=None:
			for i in range(trials):
				trial = self.runTrialV2(fitness, mStart)
				if i%(trials/10)==0:
					if self.printingOutput:
						print(i)
				totalIter += trial[0]
				if trial[1]==0:
					extinct += 1
				else:
					fixated += 1
			# print(fixated, extinct, totalIter/trials)
			# print(float(fixated)/(extinct+fixated))
			return fixated, extinct, totalIter
		else:
			print("Failed to run sim: No graph loaded")
