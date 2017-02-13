class GraphClass:
	def checkParamsValid(self, params):
		""" Takes the parameters and checks them against the expected
			types and value ranges given in metadata
			Really really need to find a way to put this into an external
			place, atm have to put this in EVERY GraphClass which is
			awful
		"""
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
