import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Star(gc.GraphClass):
	def buildGraph(self,parameters):
		convertedParams = self.checkParamsValid(parameters)
		#Check if error (Will return an error message)
		if type(convertedParams) == str:
			return convertedParams
		n = convertedParams['n']

		G = nx.Graph()
		
		for i in range(n):
			G.add_edge(0,i)
		
		return G
		

	metadata = {
		"description":"Single node connected to n-1 nodes",
		"display_name":"Star",
		"parameters":{'n': {'type': 'int'}},
		"name":"star",
	}
