import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Path(gc.GraphClass):
	def buildGraph(self,parameters):
		convertedParams = self.checkParamsValid(parameters)
		#Check if error (Will return an error message)
		if type(convertedParams) == str:
			return convertedParams
		nodes = convertedParams['nodes']

		G = nx.Graph()
		
		for i in range(nodes - 1):
			G.add_edge(i, i + 1)
		
		return G
		

	metadata = {
		"description":"path graph",
		"display_name":"Path",
		"parameters":{'nodes': {'type': 'int'}},
		"name":"path",
	}
