from simulator import Simulator
import networkx as nx
import time
import sys
import random
import os
import appgui as gui
import tkinter as tk
import fileio
import prettyoutput

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

class Controller:
	def __init__(self):
		self.graphClasses = fileio.readGraphClasses()

		self.root = tk.Tk()
		self.root.resizable(width = False, height = False)
		self.window = gui.SimSettingWindow(self.root, self)

		self.loadGraphClasses()
		print("Initialized")
		self.root.mainloop()
		print("Quitting")

	def getGraphClass(self, searchParameter, searchTerm):
		for g in self.graphClasses:
			if searchParameter in g.metadata.keys():
				if g.metadata[searchParameter]:
					if g.metadata[searchParameter] == searchTerm:
						return g
			else:
				print("{} is not a key in graphClasses".format(searchParameter))
				return -1
		print("Could not find graph with {} = {}".format(searchTerm, searchTerm))
		return -1

	def getGraphMetadata(self, searchParameter, searchTerm):
		gc = self.getGraphClass(searchParameter, searchTerm)
		if gc != -1:
			return gc.metadata
		else:
			return gc

	def getSettingsData(self, graphName):
		elements = []
		data = self.getGraphMetadata("display_name", graphName)
		
		for parameters in data['parameters']:
			elements.append((parameters,""))
		elements.append(("description", data['description']))

		return elements

	def setupAndRunSimulation(self, trialParams, graphParams, outputParams, metaTrial = False):
		graphDisplayName = graphParams['display_name']
		graphClass = self.getGraphClass("display_name", graphDisplayName)
		gc = graphClass()
		del graphParams['display_name']

		numTrials = trialParams['numTrials']
		r = trialParams['fitness']
		mStart = trialParams['startNode']
		simType = trialParams['simType']
		numBatches = trialParams['batches']

		consoleOutput = outputParams['console']
		fileOutput  = outputParams['file']
		graphOutput = outputParams['graph']

		if consoleOutput:
			verboseOutput = outputParams['verbose']
		else:
			verboseOutput = False

		G = gc.buildGraph(graphParams)

		graphSim = Simulator(consoleOutput, G)

		if verboseOutput:
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

			if verboseOutput:
				print(iterationHistograms)

			if graphOutput:
				prettyoutput.freqHistogram(iterationHistograms['fixated'])

		if consoleOutput:
			print("Average fixation over {} batches of {} trials was {}%".format(numBatches, numTrials, totalFixation * 100 / numBatches))
		else:
			print("Done")

		if fileOutput:
			print("Outputting to file")


	def createNewGraphClass(self, buildCode, metadata):
		#TODO: Validate inputs

		#All lines of build code need to be tabbed in twice
		tabbedBuildCode = ''
		for line in buildCode.split('\n'):
			tabbedBuildCode += "\n\t\t" + line
		fileio.writeNewGraphClass(tabbedBuildCode, metadata)

		try:
			reloadedGraphClasses = fileio.readGraphClasses()
			self.graphClasses = reloadedGraphClasses
			self.loadGraphClasses()
		except:
			print("Error in new graph class")
			#TODO: Handle this properly

	def loadGraphClasses(self):
		graphNames = [self.graphClasses[i].metadata['display_name'] for i in range(len(self.graphClasses))]
		self.window.populateGraphSelectListbox(graphNames)

if __name__ == "__main__":
	controller = Controller()
