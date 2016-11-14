from simulator import Simulator
import networkx as nx
import time
import sys

print("Initialized")

nodes=5000
numTrials=1000
graphType = "cycle"

G = nx.Graph()

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
	G.node[i]['mutant']=False
startTime=time.time()
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(numTrials, 5, -1)
totTime=time.time()-startTime
print(str(numTrials)+ " trials ran in " + str(totTime) + ", average trial was " + str(totTime/numTrials))
