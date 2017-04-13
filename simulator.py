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

	def resetGraphStructure(self):
		""" Resets 'mutant' and 'active' attributes for each node of the loaded graphStructure """
		if self.graphStructure == None:
			print("Tried to resetGraphStructure with no graph loaded, exiting")
			return -1
		else:
			g = self.graphStructure

			for i in range(len(g.node)):
				g.node[i]['mutant'] = False
				g.node[i]['active'] = False
			return 1

	#Basic implementation for running moran process on the graph stored in self.graphStructure
	#Scales very poorly on graphs with a large number of ndoes as the algorithm often select 'useless' nodes to reproduce that will not change the state of the graph.
	def runTrialBasic(self, fitness, mStart = -1):
		"""Naive implementation of the generalised Moran process"""
		#Initialization
		self.resetGraphStructure()
		simGraph = self.graphStructure
		numNodes = len(simGraph.node)
		if mStart == -1:
			mutantStart = random.randint(0, numNodes - 1)
		else:
			mutantStart = mStart
		simGraph.node[mutantStart]['mutant'] = True
		numMutants = 1
		numNonMutants = numNodes - 1
		iterations = 0
		uselessIterations = 0

		mutants = [mutantStart]
		nonMutants = [i for i in range(numNodes) if i != mutantStart]

		#Until mutant has fixated or gone extinct, choose a node, choose a neighbour and reproduce
		while numMutants != 0 and numNonMutants != 0:
			#All mutants are as likely to be picked as each toher, and the same for non-mutants
			#So we pick which category we want the node to come from, then pick at random from that category
			t = (numMutants * fitness) + numNonMutants
			nodeChoice = random.uniform(0, t)

			if nodeChoice > numNonMutants:
				#Pick a mutant
				nodeReproducing = mutants[random.randint(0, len(mutants) - 1)]
			else:
				#Pick a non-mutant
				nodeReproducing = nonMutants[random.randint(0, len(nonMutants) - 1)]

			n = -1
			while nodeChoice > 0:
				n += 1
				if simGraph.node[n]['mutant'] == True:
					nodeChoice -= fitness
				else:
					nodeChoice -= 1
			nodeReproducing = n

			#If the reproducing node has at least one neighbour, choose one at random (uniform probability)
			if len(simGraph.neighbors(nodeReproducing)) > 0:
				nodeDying = random.sample(simGraph.neighbors(nodeReproducing), 1)[0]
			
			if simGraph.node[nodeReproducing]['mutant'] != simGraph.node[nodeDying]['mutant']:
				simGraph.node[nodeDying]['mutant'] = simGraph.node[nodeReproducing]['mutant']
				if simGraph.node[nodeReproducing]['mutant'] == True:
					numMutants += 1
					numNonMutants -= 1
					nonMutants.remove(nodeDying)
					mutants.append(nodeDying)
				else:
					numMutants -= 1
					numNonMutants += 1
					mutants.remove(nodeDying)
					nonMutants.append(nodeDying)
			else:
				uselessIterations += 1
			iterations += 1
		return iterations, numMutants, numNonMutants

	#MAY MERGE THIS WITH THE ORIGINAL AS AN OPTION, A LOT OF CODE REPLICATION HERE
	def runTrialNodes(self, fitness, mStart = -1):
		"""	This version of runTrial keeps track of nodes with at least one neighbour of a differnet kind to themsleves.
			These nodes  are called 'active' nodes and are the only ones that ccan be selected for reproduction.
			It is still possible to get useless iterations where a node selects a neighbour of the same type, but this is much less liekly than for the naive approach, particularly for sparse graphs
		"""

		#Initialization
		self.resetGraphStructure()
		simGraph = self.graphStructure
		numNodes = len(simGraph.node)
		if mStart == -1:
			mutantStart = random.randint(0, numNodes-1)
		else:
			mutantStart = mStart
		simGraph.node[mutantStart]['mutant'] = True
		simGraph.node[mutantStart]['active'] = True
		numMutants = 1
		numNonMutants = numNodes-1
		iterations = 0
		uselessIterations = 0

		#The slight change to the method of selecting the node to reproduce (only from the active set) is the only real change from above, may want to merge together
		activeMutants = [mutantStart]
		activeNonMutants = [i for i in simGraph.neighbors(mutantStart)]
		for n in activeNonMutants:
			simGraph.node[n]['active'] = True

		while numMutants != 0 and numNonMutants != 0:
			#c is a random float from 0 - total fitness of all active nodes
			c = random.uniform(0, (len(activeMutants) * fitness) + len(activeNonMutants))

			#Each mutant/non-mutant is as likely as any other, so we just pick one set or the other then pick at random from that set
			if c > len(activeNonMutants):
				nodeReproducing = activeMutants[random.randint(0, len(activeMutants) - 1)]
			else:
				nodeReproducing = activeNonMutants[random.randint(0, len(activeNonMutants) - 1)]

			possibleDyingNodes = simGraph.neighbors(nodeReproducing)
			nodeDying = possibleDyingNodes[random.randint(0, len(possibleDyingNodes) - 1)]

			if simGraph.node[nodeReproducing]['mutant'] != simGraph.node[nodeDying]['mutant']:
				simGraph.node[nodeDying]['mutant'] = simGraph.node[nodeReproducing]['mutant']
				if simGraph.node[nodeReproducing]['mutant'] == True:
					#The new mutant must have been an activenonmutant before it died, so we move it from activeNonMutants to activeMutants
					numMutants += 1
					numNonMutants -= 1
					activeNonMutants.remove(nodeDying)

					#Check if new mutant has any non mutant neighbours - if so, isActive is true, otherwise not
					simGraph.node[nodeDying]['active'] = False
					for n in simGraph.neighbors(nodeDying):
						#If any non mutant neighbours of the new mutant were not active, they are now
						if not simGraph.node[n]['mutant']:
							simGraph.node[nodeDying]['active'] = True
							if not simGraph.node[n]['active']:
								simGraph.node[n]['active'] = True
								activeNonMutants.append(n)
						#Check whether mutant neighbour is still active
						else:
							simGraph.node[n]['active'] = False
							for nn in simGraph.neighbors(n):
								if not simGraph.node[nn]['mutant']:
									simGraph.node[n]['active'] = True
									break
							if not simGraph.node[n]['active']:
								activeMutants.remove(n)
					if simGraph.node[nodeDying]['active']:
						activeMutants.append(nodeDying)
				else:
					numMutants -= 1
					numNonMutants += 1

					activeMutants.remove(nodeDying)
					simGraph.node[nodeDying]['active'] = False

					for i in simGraph.neighbors(nodeDying):
						#All non-mutant neighbours used to be active - Check if they still are by checking whether they still have at least one non-mutant neighbour
						#This could be n^2 in the worst case, not sure how to improve
						if not simGraph.node[i]['mutant']:
							simGraph.node[i]['active'] = False

							for j in simGraph.neighbors(i):
								if simGraph.node[j]['mutant']:
									simGraph.node[i]['active'] = True
									break
							if not simGraph.node[i]['active']:
								activeNonMutants.remove(i)
						#Any mutant neighbours of the new non-mutant must now be active - set them to be so if they aren;t already
						else:
							simGraph.node[nodeDying]['active'] = True

							if not simGraph.node[i]['active']:
								simGraph.node[i]['active'] = True
								activeMutants.append(i)
					if simGraph.node[nodeDying]['active']:
						activeNonMutants.append(nodeDying)
			else:
				uselessIterations += 1
			iterations += 1
		return iterations, numMutants, numNonMutants

	def runTrialEdges(self, fitness, mStart = -1):
		""" Theorertically optimal way to run sim is to only pick useful edges - this function implements that.
			Turns out selecting a mutant becomes hard, so there isnt really any time saving (and it seems to be slower)
			on top of all that I've implemented it incorrectly and results are not valid
		"""
		self.resetGraphStructure()
		simGraph = self.graphStructure
		numNodes = len(simGraph.node)
		if mStart == -1:
			mutantStart = random.randint(0, numNodes - 1)
		else:
			mutantStart = mStart
		simGraph.node[mutantStart]['mutant'] = True
		numMutants = 1
		numNonMutants = numNodes - 1
		iterations = 0

		#Precalculating this as it takes little memory but a lookup is a lot faster than having to recalculate large bits of this every iteration
		nodeStrength = [float(1) / len(simGraph.edges(n)) for n in range(numNodes)]
		
		#activeEdges tracks all the edges between mutants and non mutants
		#To begin, this is all the edges to the initial mutant
		activeEdges = simGraph.edges(mutantStart)

		#Until mutant has fixated or gone extinct, choose a node, choose a neighbour and reproduce
		while numMutants != 0 and numNonMutants != 0:
			#The chance of selecting any given edge, (u,v), in the graph is (fitness of u/sum of all fitnesses) * (1/deg(u))
			totalWeight = 0
			edgeWeights = []

			for (u,v) in activeEdges:
				if simGraph.node[u]['mutant']:
					edgeWeightU = fitness * nodeStrength[u]
					edgeWeightV = nodeStrength[v]
				else:
					edgeWeightU = nodeStrength[u]
					edgeWeightV = fitness * nodeStrength[v]

				totalWeight += edgeWeightU + edgeWeightV

				edgeWeights.append(((u,v), edgeWeightU))
				edgeWeights.append(((v,u), edgeWeightV))

			c = random.random() * totalWeight

			for ((u, v), w) in edgeWeights:
				c -= w

				if c < 0:
					nodeReproducing = u
					nodeDying = v
					break

			simGraph.node[nodeDying]['mutant'] = simGraph.node[nodeReproducing]['mutant']

			if simGraph.node[nodeReproducing]['mutant']:
				numMutants += 1
				numNonMutants -= 1
			else: 
				numMutants -= 1
				numNonMutants += 1

			#For the node that changed, status of all edges will toggle - if active now nonactive and vice versa
			for (u, v) in simGraph.edges(nodeDying):
				if (u, v) in activeEdges:
					activeEdges.remove((u, v))
				elif (v, u) in activeEdges:
					activeEdges.remove((v, u))
				else:
					activeEdges.append((u, v))

			iterations += 1
		return iterations, numMutants, numNonMutants

	def runSim(self, trials, fitness = 2, mStart = -1, simType = 'active-nodes'):
		"""	Runs simulation of given type on the currently loaded graph type with the input mutant start node, fitness and number of trials.
			Returns the number of trials where the mutant fixated/went extinct and the total number of iterations accross all trials 
		"""
		fixated = 0
		extinct = 0
		totIter = 0

		fixatedIterationHistogram = {}
		extinctIterationHistogram = {}
		iterationHistograms = {'extinct' : extinctIterationHistogram, 'fixated' : fixatedIterationHistogram}

		if simType == 'naive':
			simFunction = self.runTrialBasic
		elif simType == 'active-nodes':
			simFunction = self.runTrialNodes
		elif simType == 'active-edges':
			simFunction = self.runTrialEdges
		else:
			print("Invalid simType passed to simulator.runSim")
			return

		if self.graphStructure != None:
			sTime = time.time()
			for i in range(trials):
				tTime = time.time()
				iterations, numMutants, numNonMutants = simFunction(fitness, mStart)

				#Mutant went extinct
				if numMutants == 0:
					if iterations in extinctIterationHistogram:
						extinctIterationHistogram[iterations] += 1
					else:
						extinctIterationHistogram[iterations] = 1
				#Mutant fixated
				else:
					if iterations in fixatedIterationHistogram:
						fixatedIterationHistogram[iterations] += 1
					else:
						fixatedIterationHistogram[iterations] = 1

				if trials > 99:
					if i % (trials / 100) == 0:
						if self.printingOutput:
							print("{}% done".format(i * 100 / trials))
				else:
					print("Trial {}/{} done".format(i + 1, trials))

				totIter += iterations
				if numMutants == 0:
					extinct += 1
				else:
					fixated += 1
			if self.printingOutput:
				totTime = time.time() - sTime
				
				print("TOOK {} SECONDS TOTAL\nAVERAGE TRIAL {} SECONDS\nAVERAGE INTREATION {} SECONDS".format(totTime, totTime / trials, totTime / totIter))
			return fixated, extinct, totIter, iterationHistograms
		else:
			print("Failed to run sim: No graph loaded")
