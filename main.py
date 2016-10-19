from simulator import Simulator
import networkx as nx
import time

print("Initialized")
startTime=time.time()
G=nx.Graph()
nodes=50
numTrials=100
for i in range(nodes-1):
	G.add_edge(i,i+1)
G.add_edge(0,nodes-1)
for i in range(len(G.node)):
	G.node[i]['mutant']=False
print("Graph created in " + str(time.time()-startTime))
startTime=time.time()
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(numTrials,1.2)
print(str(numTrials)+ " trials ran in " + str(time.time()-startTime))