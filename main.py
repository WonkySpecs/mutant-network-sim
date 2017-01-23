from simulator import Simulator
import networkx as nx
import time
import sys
import random
import os
import AppGUI as GUI
import tkinter as tk

graphTypes = []
graphClasses = []

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

def buildGraph(graphType, nodes, otherParams = None):
	G = nx.Graph()

	if graphType == "complete":
		G = nx.complete_graph(nodes)
	elif graphType == "cycle":
		for i in range(nodes - 1):
			G.add_edge(i, i + 1)
		G.add_edge(0, nodes - 1)
	elif graphType == "path":
		for i in range(nodes):
			G.add_edge(i, i + 1)

	elif graphType == "chord-cycle":
		for i in range(nodes - 1):
			G.add_edge(i, i + 1)
		G.add_edge(0, nodes - 1)
		for n in range(nodes - 1):
			for n2 in range(n + 1, nodes):
				if random.random() > 0.9:
					G.add_edge(n, n2)
	elif graphType == "urchin":
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
	elif graphType == "clique-wheel":
		n = nodes // 2
		G = nx.complete_graph(n)
		if nodes % 2==0:
			for m in range(n):
				G.add_edge(m, m + n)
			for w in range(n - 1):
				G.add_edge(w + n, w + n + 1)
			G.add_edge(n, nodes - 1)
		else:
			print("nodes must be even for a clique wheel graph")
			return
	elif graphType == "random":
		try:
			randomType = otherParams['randomType']
			p = otherParams['p']
		except:
			print("Not all parameters necessary for a random graph were passed to main.buildGraph")
			return

		if randomType == "erdos-renyi":
			G = nx.fast_gnp_random_graph(nodes, p)
			while not nx.is_connected(G):
				G = nx.fast_gnp_random_graph(nodes, p)
			print(G.edges())
			return G
	else:
		print("Invalid graphType passed to main.buildGraph")
		return

	for i in range(len(G.node)):
		G.node[i]['mutant'] = False
	return G

def setupAndRunSimulation(trialParams, graphParams, outputParams, metaTrial = False):
	numTrials = trialParams['numTrials']
	r = trialParams['fitness']
	mStart = trialParams['startNode']
	simType = trialParams['simType']
	numBatches = trialParams['batches']

	nodes = graphParams['nodes']
	graphType = graphParams['graphType']

	consoleOutput = outputParams['console']
	fileOutput  = outputParams['file']

	if graphParams['otherParams']:
		G = nx.Graph(buildGraph(graphType, nodes, graphParams['otherParams']))
	else:
		G = nx.Graph(buildGraph(graphType, nodes))

	graphSim = Simulator(consoleOutput, G)
	print("Running simulation for:")
	print(graphParams)
	print(trialParams)
	print(outputParams)
	
	totalFixation = 0
	for i in range(numBatches):
		print("--- SIMULATION {} ---\n".format(i + 1))
		fixated, extinct, totalIterations, iterationHistograms = graphSim.runSim(numTrials, r, mStart, simType)
		if consoleOutput:
			print("{} fixated, {} extinct, {} fixation, {} average iterations\n".format(fixated, extinct, fixated / (fixated + extinct), totalIterations / (fixated + extinct)))
		totalFixation += fixated / (fixated + extinct)
		print(iterationHistograms)

	if consoleOutput:
		print("Average fixation over {} batches of {} trials was {}%".format(numBatches, numTrials, totalFixation * 100 / numBatches))
	else:
		print("Done")

if __name__ == "__main__":
	print("Initialized")

	metadata = readGraphClassMetadata()
	graphNames = [metadata[i]['display_name'] for i in range(len(metadata))]
	
	root = tk.Tk()
	root.resizable(width = False, height = False)
	window = GUI.SimSettingWindow(root)

	window.populateGraphSelectListbox(graphNames)
	root.mainloop()
	print("Quitting")
