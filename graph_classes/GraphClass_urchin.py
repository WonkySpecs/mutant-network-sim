import networkx as nx

class GraphClass_urchin:
	def checkParamsValid(params):
		shouldHaveParams = [i for i in metadata[arguments].keys()]
		for k in params.keys():
			if k in shouldHaveParams:
				shouldHaveParams.remove(k)
			else:
				print("buildGraph given a parameter called {} which it should not have".format(k))
				return

		if shouldHaveParams:
			print("Necessary parameter(s) missing from buildGraph for {} graph: {}".format(metadata['name'], shouldHaveParams))
			return -1
		else:
			return 1

	def buildGraph(parameters):
		if checkParamsValid(parameters) == -1:
			return -1

		nodes = parameters['nodes']

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
		"arguments"			: {"nodes" : {'type' : 'int'}},
		"description"		: ( "nodes 0-(n/2 -1) form a clique,"
								"(n/2 - [n-1]) are an independent"
								"set, linked 1-1 with the nodes"
								" in the clique")
		}
