class GraphClass:
	def checkParamsValid(self, params):
		""" Takes the parameters and checks them against the expected
			types and value ranges given in metadata
		"""
		shouldHaveParams = [i for i in self.metadata['parameters'].keys()]
		for k in params.keys():
			if k in shouldHaveParams:
				shouldHaveParams.remove(k)
			else:
				return "buildGraph given a parameter called {} which it should not have".format(k)
				

		if shouldHaveParams:
			return "Necessary parameter(s) missing from buildGraph for {} graph: {}".format(self.metadata['name'], shouldHaveParams)

		convertedParams = dict()

		for arg in params.items():
			k = arg[0]
			v = arg[1]
			paramType = self.metadata['parameters'][k]['type']
			
			if paramType == 'int':
				try:
					convertedParams[k] = int(v)
				except:
					return "{} given as value for {}, must be an int".format(v,k)

			elif paramType == 'float':
				try:
					convertedParams[k] = float(v)
				except:
					return "{} given as value for {}, must be a float".format(v,k)
			else:
				#For now assuming everything is an int, float or str
				#Add more cases if necessary
				convertedParams[k] = [v]

		return convertedParams
