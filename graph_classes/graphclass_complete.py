import networkx as nx
import graph_classes.graphclass as gc

class GraphClass_Complete(gc.GraphClass):
	def buildGraph(self,parameters):
		convertedParams = self.checkParamsValid(parameters)

		#Check if error (Will return an error message)
		if type(convertedParams) == str:
			return convertedParams
		n = convertedParams['n']

		G = nx.complete_graph(n)
		
		return G
		

	metadata = {
		"parameters":{'n': {'type': 'int'}},
		"name":"complete",
		"description":"Complete/clique graph with n nodes",
		"display_name":"Complete",
	}
