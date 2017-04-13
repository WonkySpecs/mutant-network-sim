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
				self.errorOutput("{} is not a key in graphClasses".format(searchParameter))
				return -1
		self.errorOutput("Could not find graph with {} = {}".format(searchTerm, searchTerm))
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

		#check for error in constructing graph
		if type(G) == str:
			self.errorOutput(G)
		else:
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

				if fileOutput:
					fOut = {
						'gcname'	: graphClass.metadata['name'],
						'time'		: time.gmtime(),
						'edges'		: [edge for edge in G.edges()],
						'simType'	: simType,
						'r'			: r,
						'mStart'	: mStart,
						'results'	: {	
										'fixated'				: fixated,
										'extinct'				: extinct,
										'iterationHistograms'	: iterationHistograms,
									}
					}
					fileio.writeResultFile(fOut)
				totalFixation += fixated / (fixated + extinct)

				if verboseOutput:
					print(iterationHistograms)

				if graphOutput:
					prettyoutput.freqHistogram(iterationHistograms['fixated'])

			if consoleOutput:
				print("Average fixation over {} batches of {} trials was {}%".format(numBatches, numTrials, totalFixation * 100 / numBatches))
			else:
				print("Done")

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
			self.errorOutput("Error in new graph class")
			#TODO: Handle this properly

	def loadGraphClasses(self):
		graphNames = [self.graphClasses[i].metadata['display_name'] for i in range(len(self.graphClasses))]
		self.window.populateGraphSelectListbox(graphNames)

	def errorOutput(self, errMessage):
		print(errMessage)
		self.window.errorOutput(errMessage)

if __name__ == "__main__":
	controller = Controller()
