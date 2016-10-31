from simulator import Simulator
import networkx as nx
import time

print("Initialized")

nodes=50
numTrials=1500

#Cycle
# G=nx.Graph()
# for i in range(nodes-1):
# 	G.add_edge(i,i+1)
# G.add_edge(0,nodes-1)

#Clique
#G=nx.complete_graph(nodes)

#Clique by hand (doesnt seem to be much if any different, suspect its basically the same thing)
# G=nx.Graph()
# for i in range(nodes-1):
# 	for j in range(i+1,nodes):
# 		G.add_edge(i,j)

#Urchin
G=nx.Graph()
if nodes%2==0:
	for c in range(nodes//2-1):
		for c2 in range(c+1,nodes//2):
			G.add_edge(c,c2)
	for n in range(nodes//2):
		G.add_edge(n,n+nodes//2)
print(G.edges())

for i in range(len(G.node)):
	G.node[i]['mutant']=False
startTime=time.time()
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(numTrials,2)
totTime=time.time()-startTime
print(str(numTrials)+ " trials ran in " + str(totTime) + ", average trial was " + str(totTime/numTrials))