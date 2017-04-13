import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Biclique(gc.GraphClass):
	def buildGraph(self,parameters):
		convertedParams = self.checkParamsValid(parameters)
		#Check if error (Will return an error message)
		if type(convertedParams) == str:
			return convertedParams
		a = convertedParams['a']
		b = convertedParams['b']

		G = nx.complete_graph(a)
		
		for i in range(b - 1):
			for j in range(i + 1, b):
				G.add_edge(a + i, a + j)
		
		G.add_edge(0, a)
		
		return G
		

	metadata = {
		"description":"A clique of a nodes connected to a clique of b nodes by a single edge",
		"display_name":"Biclique",
		"name":"biclique",
		"parameters":{'a': {'type': 'int'}, 'b': {'type': 'int'}},
	}
