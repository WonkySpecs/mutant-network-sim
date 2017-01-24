import networkx as nx

class GraphClass_cycle():
	def buildGraph(nodes):
		G = nx.Graph()

		for i in range(nodes - 1):
			G.add_edge(i, i + 1)
		G.add_edge(0, nodes - 1)

		return G

	metadata = {
	"name"				: "cycle",
	"display_name"		: "Cycle",
	"argument_names"	: ["nodes",],
	"description"		: ( "Basic graph class - each node has 2 neighbours"
							"\nnodes parameter is the number of nodes")
	}
