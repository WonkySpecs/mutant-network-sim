from simulator import Simulator
import networkx as nx

print("Initialized")

G=nx.DiGraph()
G.add_edge(0,1)
G.add_edge(0,2)
G.add_edge(0,3)
G.add_edge(0,4)
G.add_edge(0,5)
for i in range(len(G.node)):
	G.node[i]['mutant']=False
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(100)