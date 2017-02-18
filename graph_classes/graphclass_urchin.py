import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Urchin(gc.GraphClass):		
	def buildGraph(self, parameters):
		convertedParams = self.checkParamsValid(parameters)

		#An error occured whilst trying to sort out parameters
		if convertedParams == -1:
			return -1

		nodes = convertedParams['nodes']

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
		"parameters"		: {"nodes" : {'type' : 'int'}},
		"description"		: ( "nodes 0-(n/2 -1) form a clique,"
								"(n/2 - [n-1]) are an independent"
								"set, linked 1-1 with the nodes"
								" in the clique")
		}
