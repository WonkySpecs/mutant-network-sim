import networkx as nx

def buildGraph(nodes):
	G = nx.Graph()

	for i in range(nodes - 1):
		G.add_edge(i, i + 1)
	G.add_edge(0, nodes - 1)

	return G
