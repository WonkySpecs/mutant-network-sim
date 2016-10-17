from simulator import Simulator
import networkx as nx

print("Initialized")

G=nx.Graph()
for i in range(49):
	G.add_edge(i,i+1)
for i in range(len(G.node)):
	G.node[i]['mutant']=False
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(10000,1.2)