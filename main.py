from simulator import Simulator
import networkx as nx

print("Initialized")

G=nx.DiGraph()
for i in range(500):
	G.add_edge(0,i)
	G.add_edge(i,0)
for i in range(len(G.node)):
	G.node[i]['mutant']=False
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(20,1.2)