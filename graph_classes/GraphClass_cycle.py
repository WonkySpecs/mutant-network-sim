import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Cycle(gc.GraphClass):
	def buildGraph(self, parameters):
		convertedParams = self.checkParamsValid(parameters)

		#An error occured whilst trying to sort out parameters
		if convertedParams == -1:
			return -1

		nodes = convertedParams['nodes']

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
