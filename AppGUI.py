import tkinter as tk
import main
from tkinter import ttk

#Map of graphType -> graphClass. Each class has a distinct set of input parameters.
#Should move this top be initialized at beginning of program from a text file so we can add graphs dynamically
graphTypeClassMap = {
	"cycle"			:	"simple" ,
	"path"			:	"simple" ,
	"urchin"		:	"simple" ,
	"clique-wheel"	:	"simple" ,
	"complete"		:	"simple" ,
	"random"		:	"random"
	}

#Lists of options for optionMenus
simTypes = [
	"naive" ,
	"active-nodes" ,
	"active-edges"]

randomGraphAlgorithms = ["erdos-renyi"]

class SimSettingWindow:
	'''	The GUI class for setting up a simulation. Allows user to select graph type and paramaters as well as trial parameters
		Validates inputs then passes inputs to main.py to handle running simulation and providing output

		All widgets are created during initialization then hidden and shown as appropriate - as there are not very many of them it is unnecessary to destroy and recreate them.
		The populate methods handle which widgets are visible'''

	def __init__(self, master):
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

		self.populateGraphSelectFrame()
		self.populateSimSettingFrame()

	#Create all widgets
	def createWidgets(self):
		#---------------- graphSettingFrame widgets------------------
		self.emptyLabel = tk.Label(self.graphSettingFrame, text = "Select a graph type")

		self.titleLabel = tk.Label(self.graphSettingFrame, text = "", justify = 'left')

		#---------------- graphSelectFrame widgets ------------------
		self.graphSelectScrollbar = tk.ttk.Scrollbar(self.graphSelectFrame)
		self.graphSelectListbox = tk.Listbox(self.graphSelectFrame, yscrollcommand = self.graphSelectScrollbar.set, selectmode = tk.SINGLE)
		self.graphSelectListbox.bind("<<ListboxSelect>>", self.populateGraphSettings)
		self.graphSelectScrollbar.config(command=self.graphSelectListbox.yview)

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

		self.startSimButton = tk.ttk.Button(self.simSettingFrame, text = "Start Simulation", command = self.validateInputAndRunSim)

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

	def populateGraphSelectListbox(self, items):
		if self.graphSelectListbox is not None:
			for item in items:
			    self.graphSelectListbox.insert(tk.END, item)
		else:
			print("Tried to populate graphListbox before it exists in SimSettingWindow")

	def populateGraphSettings(self, event):
		elements = main.getSettingsData(self.graphSelectListbox.get(self.graphSelectListbox.curselection()))
		self.populateGraphSettingFrame(elements)

	def populateGraphSettingFrame(self, elements):
		rowNum = 0
		self.deleteAllWidgetsInFrame(self.graphSettingFrame)
		graphDescriptionLabel = None

		for elementName, elementType in elements.items():
			if elementName == "description":
				graphDescriptionLabel = tk.Label(self.graphSettingFrame, anchor = tk.S, text = elementType, wraplength = 280)
			else:
				newLabel = tk.Label(self.graphSettingFrame, text = elementName)
				newEntry = tk.ttk.Entry(self.graphSettingFrame)
				newLabel.grid(in_ = self.graphSettingFrame, column = 0, row = rowNum)
				newEntry.grid(in_ = self.graphSettingFrame, column = 1, row = rowNum)
				rowNum +=1

			if graphDescriptionLabel:
				graphDescriptionLabel.grid(in_ = self.graphSettingFrame, column = 0, row = rowNum, columnspan = 2)


		#self.emptyLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0)
			

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

	def validateInputAndRunSim(self):
		''' Method called when run simulation button is clicked.
			Validates the entries for both graphSettings and simSettings then passes dictionaries of the options to setupAndRunSimulation'''

		#	-----------		Validate graph settings 	--------------
		if not hasattr(self, 'selectedGraphType'):
			print("Must select a graph type")
			return

		try:
			numNodes = int(self.numNodesEntry.get())
		except ValueError:
			print("Number of nodes must be an integer >=2")
			return

		if numNodes < 2:
			print("Must have at least 2 nodes")
			return

		#If graphType is defined, graphClass must be as well
		if self.selectedGraphClass == "simple":
			otherParams = {}
		elif self.selectedGraphClass == "random":
			try:
				p = float(self.randomGraphPEntry.get())
			except:
				print("Probability, p, must be 0<p<=1")
				return
			if p<=0 or p>1:
				print("Probability, p, must be 0<p<=1")
				return

			otherParams = { 
				'p'				: p ,
				#Because random graphclass is selected and randomGraphAlgorithmSelected is linked to an option menu,
				#it must be set to a valid option so needs no validation
				'randomType'	: self.randomGraphAlgorithmSelected.get()
				}
		else:
			print("Invalid graphClass whilst running AppGUI.validateInputAndRunSim")
			return

		graphParams = {
			'graphType' 	: self.selectedGraphType ,
			'nodes'			: numNodes ,
			'otherParams'	: otherParams
			}

		#	-----------		Validate simulation settings 	--------------
		try:
			numTrials = int(self.numTrialEntry.get())
			fitness = float(self.mutantFitnessEntry.get())
			mStart = int(self.mutantStartNodeEntry.get())
			batches = int(self.numTrialBatchesEntry.get())
		except:
			#Should probably split these up 
			print("Error with sim settings")
			return
		if numTrials < 1:
			print("Must have at least 1 trial")
			return
		if fitness <= 0:
			print("fitness cannot be zero or negative")
			return
		if mStart < -1 or mStart > numNodes - 1:
			print("Mutant start node must be between 0 and number of nodes - 1, or -1 for random")
			return
		if batches <= 0:
			print("Batches must be positive")
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

		main.setupAndRunSimulation(trialParams, graphParams, outputParams)

if __name__ == "__main__":
	metadata = main.readGraphClassMetadata()
	root = tk.Tk()
	root.resizable(width = False, height = False)
	window = SimSettingWindow(root)
	root.mainloop()
