import networkx as nx
import os
import importlib
import inspect

def readGraphClasses():
	"""Reads all of the GraphClass_*.py files from the graph_classes
		subdirectory into a list of modules which can be instantiated
		when needed. This feels hacky, but I can't think of a better
		way to do it
	"""
	classes = []
	graphClassesPath = os.path.join(os.curdir, "graph_classes")

	for filename in os.listdir(graphClassesPath):
		if filename.startswith("graphclass_") and filename.endswith(".py"):
			#Module names are of the form graph_classes/graphclass_graphtypename
			try:
				m = importlib.import_module("graph_classes." + filename[:-3])
				for c in inspect.getmembers(m, inspect.isclass):
					if testBuildGraph(c[1]):
						#This pulls the class out of the module
						classes.append(c[1])
					else:
						print("Failed to load {} graphClass, error in buildGraph function (may not be returning a graph object)".format(c[1].metadata['name']))
			except:
				print("Failed to load {}, invalid syntax in code".format(filename[:-3]))
	return classes

#This is a pretty bad hacky way of doing this, will need changing if value domains for parameters are implemented
#Could add a 'test set' of parameters to metadata to use in this method
#Also nede to hondle error emssages better
def testBuildGraph(graphClass):
	""" Tries to build a graph using the given graphClasses buildGraph
		method using test parameters
		If the graph succesfully builds, returns True, otherwise False
	"""
	try:
		gc = graphClass()
		md = gc.metadata['parameters']
		testParams = {}
		for param in md.keys():
			if md[param]['type'] == 'int':
				testParams[param] = '2'
			elif md[param]['type'] == 'float':
				testParams[param] = '0.5'
			elif md[param]['type'] == 'string':
				testParams[param] = '1'
		G = gc.buildGraph(testParams)
		if type(G) == nx.classes.graph.Graph:
			return True
		else:
			return False
	except:
		return False

def writeNewGraphClass(tabbedBuildCode, metadata):
	filename = "graphclass_" + metadata["name"] + ".py"
	path = os.path.join(os.curdir, "graph_classes", filename)
	with open(path, "w") as file:
		file.write("import networkx as nx\nimport graph_classes.graphclass as gc\n\n")
		file.write("class GraphClass_{}(gc.GraphClass):\n".format(metadata["name"].capitalize()))
		file.write("\tdef buildGraph(self,parameters):\n")
		file.write("\t\tconvertedParams = self.checkParamsValid(parameters)\n")
		file.write("\t\tif type(convertedParams) == str:\n\t\t\treturn convertedParams\n")
		for param in metadata['parameters'].keys():
			file.write("\t\t{} = convertedParams['{}']\n".format(param, param))
		file.write(tabbedBuildCode)
		file.write("\n\n\tmetadata = {")
		for key, value in metadata.items():
			#Arguments are all written as strings except for parameters which is a dictionary
			if key == "parameters":
				file.write('\n\t\t"{}":{},'.format(key, value))
			else:
				file.write('\n\t\t"{}":"{}",'.format(key, value))
		file.write("\n\t}")


def saveGraph(G, graphName):
	graphsPath = os.path.join(os.curdir, "results", "graphs")

	if not os.path.exists(graphsPath):
		os.makedirs(graphsPath)

	graphName += ".gml"

	toSave = True

	if os.path.isfile(os.path.join(graphsPath, graphName)):
		i = ""
		while i != "y" and i != "n":
			print("File already exists - Overwrite? y/n")
			i = input().lower()

		if i == "n":
			toSave = False
			print("Aborting save")

	if toSave:
		print("Saving")
		nx.write_gml(G, os.path.join(graphsPath, graphName))

def writeResultFile(output):
	resultsPath = os.path.join(os.curdir, "results", output['gcname'])

	if not os.path.exists(resultsPath):
		os.makedirs(resultsPath)

	#parse outputs
	filename = output['gcname'] + str(len([f for f in os.listdir(resultsPath)]))
	print("Writing " + filename)
	
	with open(os.path.join(resultsPath, filename), "w") as outFile:
		for key, value in output.items():
			outFile.write(key + ",")
			outFile.write(repr(value) +"\n")

