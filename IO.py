import networkx as nx
import os

def saveGraph(G, graphName):
	if not os.path.exists("results"):
		os.makedirs("results")

	graphsPath = os.path.join(os.curdir, "results", "graphs")

	if not os.path.exists(graphsPath):
		os.makedirs(graphsPath)

	graphName += ".gml"

	nx.write_gml(G, os.path.join(graphsPath, graphName))

saveGraph(nx.path_graph(4), "path-4")
