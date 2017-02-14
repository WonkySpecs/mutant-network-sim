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
			m = importlib.import_module("graph_classes." + filename[:-3])

			#This pulls the class out of the module
			for c in inspect.getmembers(m, inspect.isclass):
				classes.append(c[1])

	return classes

def writeNewGraphClass(buildCode, metadata):
	filename = "graphclass_" + metadata["name"] + ".py"
	path = os.path.join(os.curdir, "graph_classes", filename)
	with open(path, "w") as file:
		file.write("import networkx as nx\nimport graph_classes.graphclass as gc\n\n")
		file.write("class GraphClass_{}:\n\t".format(metadata["name"].capitalize()))
		file.write("def buildGraph(")
		#for param in metadata["parameters"].keys():
		#	write the parameter and comma
		file.write("):\n\t\t")
		file.write(buildCode)
		file.write("\n\n\tmetadata = {")
		for key, value in metadata.items():
			file.write('\n\t\t"{}":"{}"'.format(key, value))
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

def saveResults(output):
	experimentsPath = os.path.join(os.curdir, "results", "experiments")

	if not os.path.exists(experimentsPath):
		os.makedirs(experimentsPath)

	#parse outputs
	filename = output['filename']
	content = output['content']
	with open(os.path.join(experimentsPath, filename), "w") as outFile:
		outFile.write(content)
