import tkinter as tk
from tkinter import ttk

#Lists of options for optionMenus
simTypes = [
	"naive" ,
	"active-nodes" ,
	"active-edges"]

randomGraphAlgorithms = ["erdos-renyi"]

class SimSettingWindow:
	'''	The GUI class for setting up a simulation. Allows user to select graph type and parameters as well as trial parameters
		Validates inputs then passes inputs to main.py to handle running simulation and providing output
		'''

	def __init__(self, master, controller):
		self.controller = controller
		self.master = master

		self.master.grid_columnconfigure(1, minsize = 280)
		self.master.grid_columnconfigure(2, minsize = 220)

		#Set up frames
		self.graphSelectFrame = tk.Frame(self.master)
		self.graphSelectFrame.grid(column = 0, row = 0)

		self.graphSettingFrame = tk.Frame(self.master)
		self.graphSettingFrame.grid(column = 1, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)

		self.simSettingFrame = tk.Frame(self.master)
		self.simSettingFrame.grid(column = 2, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)

		self.createWidgets()
		self.selectedGraphClassName = None

		self.populateGraphSelectFrame()
		self.populateGraphSettingFrame(None)
		self.populateSimSettingFrame()

	#Create all widgets
	def createWidgets(self):
		#---------------- graphSettingFrame widgets------------------
		self.emptyLabel = tk.Label(self.graphSettingFrame, text = "Select a graph type")

		#---------------- graphSelectFrame widgets ------------------
		self.graphSelectScrollbar = tk.ttk.Scrollbar(self.graphSelectFrame)
		self.graphSelectListbox = tk.Listbox(self.graphSelectFrame, yscrollcommand = self.graphSelectScrollbar.set, selectmode = tk.SINGLE)
		self.graphSelectListbox.bind("<<ListboxSelect>>", self.populateGraphSettings)
		self.graphSelectScrollbar.config(command=self.graphSelectListbox.yview)
		self.createGraphClassButton = tk.ttk.Button(self.graphSelectFrame, text = "New graph class", command = self.newGraphClassWindow)

		#---------------- simSettingFrame widgets  ------------------
		self.numTrialLabel = tk.Label(self.simSettingFrame, text = "Number of trials:")
		self.numTrialEntry = tk.ttk.Entry(self.simSettingFrame)
		self.numTrialEntry.insert(tk.END, '1000')

		self.mutantFitnessLabel = tk.Label(self.simSettingFrame, text = "Mutant relative fitness:")
		self.mutantFitnessEntry = tk.ttk.Entry(self.simSettingFrame)
		self.mutantFitnessEntry.insert(tk.END, '2')

		self.mutantStartNodeLabel = tk.Label(self.simSettingFrame, text = "Mutant start node:")
		self.mutantStartNodeEntry = tk.ttk.Entry(self.simSettingFrame)
		self.mutantStartNodeEntry.insert(tk.END, '-1')

		self.simTypeSelected = tk.StringVar(self.master)
		self.simulationTypeLabel = tk.Label(self.simSettingFrame, text = "Simulation type:")
		self.simulationTypeOptionMenu = tk.ttk.OptionMenu(self.simSettingFrame, self.simTypeSelected, simTypes[0], *simTypes)

		self.numTrialBatchesLabel = tk.Label(self.simSettingFrame, text = "Trial batches:")
		self.numTrialBatchesEntry = tk.ttk.Entry(self.simSettingFrame)
		self.numTrialBatchesEntry.insert(tk.END, '1')

		self.outputToConsole = tk.IntVar(self.master)
		self.outputToConsole.set(1)
		self.consoleOutputCheck = tk.Checkbutton(self.simSettingFrame, text = "Console output", variable = self.outputToConsole)
		self.outputToFile = tk.IntVar(self.master)
		self.fileOutputCheck = tk.Checkbutton(self.simSettingFrame, text = "File output", variable = self.outputToFile)

		self.startSimButton = tk.ttk.Button(self.simSettingFrame, text = "Start Simulation", command = self.collectInputsAndRunSim)

	def hideAllWidgetsInFrame(self, frame):
		for child in frame.winfo_children():
			child.grid_forget()

	def deleteAllWidgetsInFrame(self, frame):
		for child in frame.winfo_children():
			child.destroy()

	def populateGraphSelectFrame(self):
		self.hideAllWidgetsInFrame(self.graphSelectFrame)
		self.graphSelectScrollbar.grid(column = 1, row = 0, sticky = tk.N + tk.S)
		self.graphSelectListbox.grid(column = 0, row = 0, sticky = tk.W + tk.N + tk.S, padx = 3, pady = 1)
		self.createGraphClassButton.grid(column = 0, row = 1, sticky = tk.E + tk.S + tk.W)

	#Could generalise this to fill any arbitrary listbox/optionmenu/entry
	def populateGraphSelectListbox(self, items):
		if self.graphSelectListbox is not None:
			for item in items:
			    self.graphSelectListbox.insert(tk.END, item)
		else:
			print("Tried to populate graphListbox before it exists in SimSettingWindow")

	def populateGraphSettings(self, event):
		#Gives the currently selected graph type to main.getSettingsData which finds the correct set of metadata
		#for that graph class and returns the list of parameters needed to create one
		self.selectedGraphClassName = self.graphSelectListbox.get(self.graphSelectListbox.curselection())
		elements = self.controller.getSettingsData(self.selectedGraphClassName)
		self.populateGraphSettingFrame(elements)

	def populateGraphSettingFrame(self, elements):
		self.graphSettingParameterEntryLabelTexts = []
		self.graphSettingParameterEntries = []
		if elements:
			self.deleteAllWidgetsInFrame(self.graphSettingFrame)
			titleLabel = tk.Label(self.graphSettingFrame, text = self.selectedGraphClassName, justify = 'left')
			titleLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0, sticky = tk.W + tk.N)
			rowNum = 1
			graphDescriptionLabel = None

			for (elementName, elementType) in elements:
				if elementName == "description":
					graphDescriptionLabel = tk.Label(self.graphSettingFrame, anchor = tk.S, text = elementType, wraplength = 270)
				else:
					newLabel = tk.Label(self.graphSettingFrame, text = elementName)
					newEntry = tk.ttk.Entry(self.graphSettingFrame)
					newLabel.grid(in_ = self.graphSettingFrame, column = 0, row = rowNum)
					newEntry.grid(in_ = self.graphSettingFrame, column = 1, row = rowNum)
					self.graphSettingParameterEntryLabelTexts.append(elementName)
					self.graphSettingParameterEntries.append(newEntry)
					rowNum += 1

			if graphDescriptionLabel:
				graphDescriptionLabel.grid(in_ = self.graphSettingFrame, column = 0, row = rowNum, columnspan = 2)
		else:
			self.emptyLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0)			

	def populateSimSettingFrame(self):
		self.hideAllWidgetsInFrame(self.simSettingFrame)
		self.numTrialLabel.grid(in_ = self.simSettingFrame, column = 0, row = 0, sticky = tk.W)
		self.numTrialEntry.grid(in_ = self.simSettingFrame, column = 1, row = 0)

		self.mutantFitnessLabel.grid(in_ = self.simSettingFrame, column = 0, row = 1, sticky = tk.W)
		self.mutantFitnessEntry.grid(in_ = self.simSettingFrame, column = 1, row = 1)

		self.mutantStartNodeLabel.grid(in_ = self.simSettingFrame, column = 0, row = 2, sticky = tk.W)
		self.mutantStartNodeEntry.grid(in_ = self.simSettingFrame, column = 1, row = 2)

		self.simulationTypeLabel.grid(in_ = self.simSettingFrame, column = 0, row = 3, sticky = tk.W)
		self.simulationTypeOptionMenu.grid(in_ = self.simSettingFrame, column = 1, row = 3, sticky = tk.W)

		self.numTrialBatchesLabel.grid(in_ = self.simSettingFrame, column = 0, row = 4, sticky = tk.W)
		self.numTrialBatchesEntry.grid(in_ = self.simSettingFrame, column = 1, row = 4)

		self.consoleOutputCheck.grid(in_ = self.simSettingFrame, column = 0, row = 5)
		self.fileOutputCheck.grid(in_ = self.simSettingFrame, column = 1, row = 5)

		self.startSimButton.grid(in_ = self.simSettingFrame, column = 0, columnspan = 2)

	def getGraphSettings(self):
		graphSettings = dict()
		
		for i in range(len(self.graphSettingParameterEntryLabelTexts)):
			parameterName = self.graphSettingParameterEntryLabelTexts[i]
			parameterValue = self.graphSettingParameterEntries[i].get()
			graphSettings[parameterName] = parameterValue

		graphSettings['display_name'] = self.selectedGraphClassName

		return graphSettings

	def newGraphClassWindow(self):
		root2 = tk.Tk()
		root2.resizable(width = False, height = False)
		gccw = GraphClassCreateWindow(root2, self.controller)
		root2.mainloop()

	def collectInputsAndRunSim(self):
		''' Method called when run simulation button is clicked.
			Validates the entries for both graphSettings and simSettings then passes dictionaries of the options to setupAndRunSimulation'''

		#	-----------		Get graph settings 	--------------
		graphParams = self.getGraphSettings()

		#	-----------		Get and validate simulation settings 	--------------
		try:
			numTrials = int(self.numTrialEntry.get())
			fitness = float(self.mutantFitnessEntry.get())
			mStart = int(self.mutantStartNodeEntry.get())
			batches = int(self.numTrialBatchesEntry.get())
		except:
			#Should probably split these up 
			print("Error with sim settings")
			return

		trialParams = {
			'numTrials' : numTrials ,
			'fitness'	: fitness ,
			'startNode' : mStart ,
			#No validation needed, same as randomGraphAlgorithmSelected above
			'simType'	: self.simTypeSelected.get() ,
			'batches'	: batches
			}

		outputParams = {
			'console'	: self.outputToConsole.get() ,
			'file'		: self.outputToFile.get()
			}

		self.controller.setupAndRunSimulation(trialParams, graphParams, outputParams)

class GraphClassCreateWindow:
	def __init__(self, master, controller):
		self.master = master
		self.controller = controller

		rowNum = 0

		self.nameLabel = tk.Label(self.master, text = "Graph class name:")
		self.nameEntry = tk.ttk.Entry(self.master, width = 40)
		self.nameLabel.grid(in_ = self.master, row = rowNum, column = 0, sticky = tk.W)
		self.nameEntry.grid(in_ = self.master, row = rowNum, column = 1, sticky = tk.W)
		self.helpButton = tk.ttk.Button(self.master, text = "Help", command = self.openHelp)
		self.helpButton.grid(in_ = self.master, row = rowNum, column = 2)
		rowNum +=1

		self.parameterLabel = tk.ttk.Label(self.master, text = "This is where the parameter stuff goes somehow")
		self.parameterLabel.grid(in_ = self.master, row = rowNum, column = 0, sticky = tk.W)
		rowNum +=1

		self.buildCodeLabel = tk.Label(self.master, text = "Build function code:")
		self.buildCodeLabel.grid(in_ = self.master, row = rowNum, sticky = tk.W)
		rowNum +=1

		self.buildCodeText = tk.Text(self.master, width = 70, height = 28)
		self.buildCodeText.grid(in_ = self.master, row = rowNum, columnspan = 3)
		rowNum +=1

		self.descriptionLabel = tk.Label(self.master, text = "Description:")
		self.descriptionEntry = tk.ttk.Entry(self.master, width = 40)
		self.descriptionLabel.grid(in_ = self.master, row = rowNum, column = 0, sticky = tk.W)
		self.descriptionEntry.grid(in_ = self.master, row = rowNum, column = 1, sticky = tk.W)
		rowNum += 1

		self.submitButton = tk.ttk.Button(self.master, text = "Create class", command = self.createGraphClass)
		self.submitButton.grid(in_ = self.master, row = rowNum, columnspan = 2)

	def createGraphClass(self):
		buildCode = self.buildCodeText.get(1.0, tk.END)
		metadata = self.compileMetadata()
		self.controller.createNewGraphClass(buildCode, metadata)
		self.master.destroy()

	def compileMetadata(self):
		md = dict()
		name = self.nameEntry.get()
		desc = self.descriptionEntry.get()

		#TODO: validate inputs, get parameter names

		md['name'] = name
		md['display_name'] = name.capitalize()
		md['description'] = desc
		
		return md

	def openHelp(self):
		print("Help text")

if __name__ == "__main__":
	m = tk.Tk()
	w = GraphClassCreateWindow(m, "qwe")
	m.mainloop()
