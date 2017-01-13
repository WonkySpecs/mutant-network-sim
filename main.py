from simulator import Simulator
import networkx as nx
#import matplotlib.pyplot as plt
import time
import sys
import random

print("Initialized")

def buildGraph(graphType, nodes, otherParams = None):
	G = nx.Graph()

	if graphType == "complete":
		G = nx.complete_graph(nodes)
	elif graphType == "cycle":
		for i in range(nodes - 1):
			G.add_edge(i, i + 1)
		G.add_edge(0,nodes - 1)
	elif graphType == "path":
		for i in range(nodes):
			G.add_edge(i, i + 1)

	elif graphType == "chord-cycle":
		for i in range(nodes - 1):
			G.add_edge(i,i + 1)
		G.add_edge(0,nodes - 1)
		for n in range(nodes - 1):
			for n2 in range(n + 1, nodes):
				if random.random() > 0.9:
					G.add_edge(n, n2)
	elif graphType == "urchin":
		G = nx.Graph()
		n = nodes // 2
		if nodes%2 == 0:
			for c in range(n - 1):
				for c2 in range(c + 1, n):
					G.add_edge(c, c2)
			for m in range(n):
				G.add_edge(m, m + n)
		else:
			print("nodes must be even for an Urchin graph")
			return
	elif graphType == "clique-wheel":
		n = nodes // 2
		G = nx.complete_graph(n)
		if nodes%2==0:
			for m in range(n):
				G.add_edge(m, m + n)
			for w in range(n - 1):
				G.add_edge(w + n, w + n + 1)
			G.add_edge(n, nodes - 1)
		else:
			print("nodes must be even for a clique wheel graph")
			return
	elif graphType == "random":
		try:
			randomType = otherParams['randomType']
			p = otherParams['p']
		except:
			print("Not all parameters necessary for a random graph were passed to main.buildGraph")
			return

		if randomType == "erdos-renyi":
			G = nx.fast_gnp_random_graph(nodes, p)
			while not nx.is_connected(G):
				G = nx.fast_gnp_random_graph(nodes, p)
			print(G.edges())
			return G
	else:
		print("Invalid graphType passed to main.buildGraph")
		return

	for i in range(len(G.node)):
		G.node[i]['mutant'] = False
	return G

def setupAndRunSimulation(trialParams, graphParams, outputParams, metaTrial = False):
	numTrials = trialParams['numTrials']
	r = trialParams['fitness']
	mStart = trialParams['startNode']
	simType = trialParams['simType']
	numBatches = trialParams['batches']

	nodes = graphParams['nodes']
	graphType = graphParams['graphType']
	if graphParams['otherParams']:
		G = nx.Graph(buildGraph(graphType, nodes, graphParams['otherParams']))
	else:
		G = nx.Graph(buildGraph(graphType, nodes))

	if outputParams['outputType'] == 'simple':
		printOutput = True
	else:
		printOutput = False

	graphSim = Simulator(printOutput)
	graphSim.loadGraphStructure(G)
	print("Running simulation for:")
	print(graphParams)
	print(trialParams)
	print(G.edges())

	totalFixation = 0
	for i in range(numBatches):
		print("--- SIMULATION {} ---\n".format(i + 1))
		fixated, extinct, iterations = graphSim.runSim(numTrials, r, mStart, simType)
		print("{} fixated, {} extinct, {} fixation, {} average iterations\n".format(fixated, extinct, fixated / (fixated + extinct), iterations / (fixated + extinct)))
		totalFixation += fixated / (fixated + extinct)

	print("Average fixation over {} batches of {} trials was {}%".format(numBatches, numTrials, totalFixation * 100 / numBatches))

if __name__ == "__main__":
	nodes = 600
	numTrials = 500
	graphType = "complete"

	G = nx.Graph(buildGraph(graphType, nodes))
	# nx.draw(G)
	# plt.draw()
	# plt.show()
	graphSim=Simulator(True)
	graphSim.loadGraphStructure(G)

	startTime=time.time()
	fixated, extinct, iterations = graphSim.runSim(numTrials, 5, 70)

	print("{} fixated, {} extinct, {} fixation\nTook {} seconds".format(fixated, extinct, fixated/(fixated+extinct), time.time() - startTime))

#For running many batches of trials
# metaNumTrials = 500
# totalDiff = 0
# fixation = 0
# maxDiff = 0
# minDiff = 1
# r = 1.1
# for i in range(metaNumTrials):
# 	expectedF = 1 - 1/r
# 	fixated, extinct, iterations = graphSim.runSim(numTrials, r, 0)
# 	fixation += fixated
# 	actualF = float(fixated)/numTrials
# 	diff = abs(actualF - expectedF)
# 	if diff > maxDiff:
# 		maxDiff = diff
# 	if diff < minDiff:
# 		minDiff = diff
# 	totalDiff += diff
# 	print(i)
# averageDiff = float(totalDiff)/metaNumTrials
# print("Average diff = {}, maxDiff = {}, minDiff = {}, total fixation rate was {}".format(averageDiff, maxDiff, minDiff, float(fixation)/(metaNumTrials*numTrials)))
# totTime=time.time()-startTime
# print(str(numTrials)+ " trials ran in " + str(totTime) + ", average trial was " + str(totTime/numTrials))
