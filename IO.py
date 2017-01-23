import networkx as nx
import os

def readGraphClassMetadata():
	data = []
	graphClassesPath = os.path.join(os.curdir, "graph_classes")

	for subdir in os.listdir(graphClassesPath):
		containsMetadata = False
		containsBuildCode = False
		containsRubbish = False

		subpath = os.path.join(graphClassesPath, subdir)
		for filename in os.listdir(subpath):
			if filename == "metadata.txt":
				containsMetadata = True
				with open(os.path.join(subpath, "metadata.txt"), "r") as f:
					s = f.read()
					#metadata files assign a dictionary containing all meta data for a graphclass to a variable called 'metadata'
					exec(s)
					data.append(metadata)

			elif filename == "build_code.py":
				containsBuildCode = True
			else:
				containsRubbish = True

		if containsRubbish:
			print("{} contains unused file(s)".format(subpath))
		if not containsMetadata:
			print("Metadata not found in {}".format(subpath))
		if not containsBuildCode:
			#TODO: Add funcitonality to remove metadata if build code does not exist
			print("Build code not found in {}".format(subpath))
	return data

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

if __name__ == "__main__":
	saveGraph(nx.path_graph(4), "path-4")
	saveResults({"filename":"r1.result", "content":"I'm so appalled"})
