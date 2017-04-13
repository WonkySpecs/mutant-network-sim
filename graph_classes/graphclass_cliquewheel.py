import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Cliquewheel(gc.GraphClass):
	def buildGraph(self,parameters):
		convertedParams = self.checkParamsValid(parameters)
		#Check if error (Will return an error message)
		if type(convertedParams) == str:
			return convertedParams
		nodes = convertedParams['nodes']

		n = nodes // 2
		G = nx.complete_graph(n)
		if nodes % 2==0:
			for m in range(n):
				G.add_edge(m, m + n)
			for w in range(n - 1):
				G.add_edge(w + n, w + n + 1)
			G.add_edge(n, nodes - 1)
		else:
			print("nodes must be even for a clique wheel graph")
			return

		return G
		

	metadata = {
		"description":"Nodes 0 to (nodes//2 -1) are a clique with a 1-1 mapping to the nodes (nodes//2) to (nodes -1) which form a cycle",
		"display_name":"Cliquewheel",
		"name":"cliquewheel",
		"parameters":{'nodes': {'type': 'int'}},
	}
