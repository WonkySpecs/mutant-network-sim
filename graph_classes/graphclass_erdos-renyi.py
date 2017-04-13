import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Erdosrenyi(gc.GraphClass):
	def buildGraph(self,parameters):
		convertedParams = self.checkParamsValid(parameters)
		#Check if error (Will return an error message)
		if type(convertedParams) == str:
			return convertedParams
		p = convertedParams['p']
		n = convertedParams['n']

		G = nx.fast_gnp_random_graph(n, p)
		while not nx.is_connected(G):
			G = nx.fast_gnp_random_graph(n, p)
		return G
		

	metadata = {
		"name":"erdosrenyi",
		"display_name":"Erdos-Renyi",
		"description":"Random graph with n nodes and connection probability p built with the Erdos-Renyi algorithm.",
		"parameters":{'p': {'type': 'float'}, 'n': {'type': 'int'}},
	}
