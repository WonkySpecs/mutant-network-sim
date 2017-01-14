import networkx as nx
import os

def saveGraph(G, graphName):
	graphsPath = os.path.join(os.curdir, "results", "graphs")

	if not os.path.exists(graphsPath):
		os.makedirs(graphsPath)

	graphName += ".gml"

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

saveGraph(nx.path_graph(4), "path-4")
saveResults({"filename":"r1.result", "content":"I'm so appalled"})
