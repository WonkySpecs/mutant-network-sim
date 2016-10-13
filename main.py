from simulator import Simulator
import networkx as nx

print("Initialized")

G=nx.DiGraph()

graphSim=Simulator()
graphSim.loadGraphStructure(G)
graphSim.runSim(100)