from simulator import Simulator
import networkx as nx
import time
import sys

print("Initialized")

def buildGraph(graphType, nodes):
	G = nx.Graph()

	if graphType in nx.generators.classic.__all__:
		#Very cool but sketchy - not all of these methods only take a 'nodes' argument, probably need to hard code a few more things here. Works for wheel graph at least
		G = getattr(nx.generators.classic, graphType)(nodes)
	else:
		if graphType == "complete":
			G = nx.complete_graph(nodes)

		elif graphType == "cycle":
			for i in range(nodes-1):
				G.add_edge(i,i+1)
			G.add_edge(0,nodes-1)

		elif graphType == "urchin":
			G = nx.Graph()
			n = nodes//2
			if nodes%2==0:
				for c in range(n-1):
					for c2 in range(c+1,n):
						G.add_edge(c,c2)
				for m in range(n):
					G.add_edge(m,m+n)
			else:
				print("nodes must be even for an Urchin graph")
				sys.exit()

		elif graphType == "clique-wheel":
			n = nodes//2
			G = nx.complete_graph(n)
			if nodes%2==0:
				for m in range(n):
					G.add_edge(m, m + n)
				for w in range(n - 1):
					G.add_edge(w+n ,w+n+1)
				G.add_edge(n, nodes - 1)
			else:
				print("nodes must be even for a clique wheel graph")
				sys.exit()

	for i in range(len(G.node)):
		G.node[i]['mutant'] = False
	return G

nodes=500
numTrials=100
graphType = "wheel_graph"

G = nx.Graph(buildGraph(graphType, nodes))

#startTime=time.time()
graphSim=Simulator(False)
graphSim.loadGraphStructure(G)

metaNumTrials = 500
totalDiff = 0
fixation = 0
maxDiff = 0
minDiff = 1
r = 1.1
for i in range(metaNumTrials):
	expectedF = 1 - 1/r
	fixated, extinct, iterations = graphSim.runSim(numTrials, r, 0)
	fixation += fixated
	actualF = float(fixated)/numTrials
	diff = abs(actualF - expectedF)
	if diff > maxDiff:
		maxDiff = diff
	if diff < minDiff:
		minDiff = diff
	totalDiff += diff
	print(i)
averageDiff = float(totalDiff)/metaNumTrials
print("Average diff = {}, maxDiff = {}, minDiff = {}, total fixation rate was {}".format(averageDiff, maxDiff, minDiff, float(fixation)/(metaNumTrials*numTrials)))	
# totTime=time.time()-startTime
# print(str(numTrials)+ " trials ran in " + str(totTime) + ", average trial was " + str(totTime/numTrials))
