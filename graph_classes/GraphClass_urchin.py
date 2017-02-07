import networkx as nx

class GraphClass_urchin():
	def checkParamsValid(self, params):
		shouldHaveParams = [i for i in self.metadata['arguments'].keys()]
		for k in params.keys():
			if k in shouldHaveParams:
				shouldHaveParams.remove(k)
			else:
				print("buildGraph given a parameter called {} which it should not have".format(k))
				return

		if shouldHaveParams:
			print("Necessary parameter(s) missing from buildGraph for {} graph: {}".format(self.metadata['name'], shouldHaveParams))
			return -1

		convertedParams = dict()

		for arg in params.items():
			k = arg[0]
			v = arg[1]
			paramType = self.metadata['arguments'][k]['type']
			
			if paramType == 'int':
				try:
					convertedParams[k] = int(v)
				except TypeError:
					print("{} given as value for {} in urchin, must be an int".format(v,k))
					return -1
			elif paramType == 'float':
				try:
					convertedParams[k] = float(v)
				except TypeError:
					print("{} given as value for {} in urchin, must be a float".format(v,k))
					return -1
			else:
				#For now assuming everything is an int, float or str
				#Add more cases if necessary
				convertedParams[k] = [v]

		return convertedParams
		
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
		"arguments"			: {"nodes" : {'type' : 'int'}},
		"description"		: ( "nodes 0-(n/2 -1) form a clique,"
								"(n/2 - [n-1]) are an independent"
								"set, linked 1-1 with the nodes"
								" in the clique")
		}
