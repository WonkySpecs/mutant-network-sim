import networkx as nx

class GraphClass_urchin:
	def buildGraph(nodes):
		G = nx.Graph()
		n = nodes // 2
		if nodes % 2 == 0:
			for c in range(n - 1):
				for c2 in range(c + 1, n):
					G.add_edge(c, c2)
			for m in range(n):
				G.add_edge(m, m + n)
		else:
			print("nodes must be even for an Urchin graph")
			return

		return G

	metadata = {
		"name"				: "urchin",
		"display_name"		: "Urchin",
		"argument_names"	: ["nodes",],
		"description"		: ( "A graph with n nodes arranged with half"
								" in a clique and the other half in an "
								"independent set, with each"
								" clique node connected to exactly one "
								"node in the independent set"
								"\nFor mutant start node, use -1 for random"
								"start, in the range 0-(n/2 -2) for a node "
								"in the clique and n/2 - (n-1) for a nose"
								"\nMust have an even number of nodes")
		}
