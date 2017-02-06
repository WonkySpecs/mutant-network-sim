import networkx as nx

class GraphClass_cycle():
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

		for i in range(nodes - 1):
			G.add_edge(i, i + 1)
		G.add_edge(0, nodes - 1)

		return G

	metadata = {
	"name"				: "cycle",
	"display_name"		: "Cycle",
	"arguments"			: {"nodes" : {'type' : 'int'}},
	"description"		: ( "Basic graph class - each node has 2 neighbours"
							"\nnodes parameter is the number of nodes")
	}
