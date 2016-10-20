from simulator import Simulator
import networkx as nx
import time

print("Initialized")
G=nx.Graph()
nodes=50
numTrials=100
for i in range(nodes-1):
	G.add_edge(i,i+1)
G.add_edge(0,nodes-1)
for i in range(len(G.node)):
	G.node[i]['mutant']=False
startTime=time.time()
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(numTrials,1.2)
totTime=time.time()-startTime
print(str(numTrials)+ " trials ran in " + str(totTime) + ", average trial was " + str(totTime/numTrials))