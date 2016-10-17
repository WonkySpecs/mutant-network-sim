from simulator import Simulator
import networkx as nx

print("Initialized")

G=nx.Graph()
nodes=50
for i in range(nodes-1):
	G.add_edge(i,i+1)
G.add_edge(0,nodes-1)
for i in range(len(G.node)):
	G.node[i]['mutant']=False
graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(5000,1.2)