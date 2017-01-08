import tkinter as tk
from tkinter import ttk

#Map of graphType -> graphClass. Each class has a distinct set of input parameters.
graphTypeClassMap = {
					"cycle":"simple",
					"path":"simple",
					"urchin":"simple",
					"clique-wheel":"simple",
					"complete":"simple",
					"random":"random"
					 }

class SimSettingWindow:
	'''	The GUI class for setting up a simulation. Allows user to select graph type and paramaters as well as trial parameters
		Validates inputs then passes inputs to main.py to handle running simulation and providing output

		All widgets are created during initialization then hidden and shown as appropriate - as there are not very many of them it is unnecessary to destroy and recreate them.
		The populate methods handle which widgets are visible'''

	def __init__(self, master):
		self.master = master

		self.master.grid_columnconfigure(1, minsize = 250)
		self.master.grid_columnconfigure(2, minsize = 250)

		#Set up frames
		self.graphSelectFrame = tk.Frame(self.master)
		self.graphSelectFrame.grid(column = 0, row = 0)

		self.graphSettingFrame = tk.Frame(self.master)
		self.graphSettingFrame.grid(column = 1, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)

		self.simSettingFrame = tk.Frame(self.master)
		self.simSettingFrame.grid(column = 2, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)

		self.createWidgets()

		self.populateGraphSelectFrame()
		self.populateGraphSettingFrame()		
		self.populateSimSettingFrame()
		self.populateGraphSelectListbox()

	#Create all widgets
	def createWidgets(self):
		#---------------- graphSettingFrame widgets------------------
		self.emptyLabel = tk.Label(self.graphSettingFrame, text = "Select a graph type")

		self.titleLabel = tk.Label(self.graphSettingFrame, text = "", justify = 'left')

		self.nodeNumLabel = tk.Label(self.graphSettingFrame, text = "Number of nodes:")
		self.nodeNumEntry = tk.ttk.Entry(self.graphSettingFrame)

		self.label2 = tk.Label(self.graphSettingFrame, text = "Something else:")

		self.entry2 = tk.ttk.Entry(self.graphSettingFrame)

		#---------------- graphSelectFrame widgets ------------------
		self.graphSelectScrollbar = tk.ttk.Scrollbar(self.graphSelectFrame)
		self.graphSelectListbox = tk.Listbox(self.graphSelectFrame, yscrollcommand = self.graphSelectScrollbar.set, selectmode = tk.SINGLE)
		self.graphSelectListbox.bind("<<ListboxSelect>>",self.graphSettingSetup)
		self.graphSelectScrollbar.config(command=self.graphSelectListbox.yview)

		#---------------- simSettingFrame widgets  ------------------
		self.numTrialLabel = tk.Label(self.simSettingFrame, text = "Number of trials:")
		self.numTrialEntry = tk.ttk.Entry(self.simSettingFrame)
		self.startSimButton = tk.ttk.Button(self.simSettingFrame, text = "Start Simulation", command = self.validateInputAndRunSim)

	def hideAllWidgetsInFrame(self, frame):
		for child in frame.winfo_children():
			child.grid_forget()

	def populateGraphSelectFrame(self):
		self.hideAllWidgetsInFrame(self.graphSelectFrame)
		self.graphSelectScrollbar.grid(column = 1, row = 0, sticky = tk.N + tk.S)
		self.graphSelectListbox.grid(column = 0, row = 0, sticky = tk.W + tk.N + tk.S, padx = 3, pady = 1)

	def populateGraphSelectListbox(self):
		if self.graphSelectListbox is not None:
			for item in graphTypeClassMap.keys():#["Cycle", "Path", "Urchin", "Clique-wheel", "Complete", "Random"]:
			    self.graphSelectListbox.insert(tk.END, item)
		else:
			print("Tried to populate graphListbox before it exists in SimSettingWindow")

	def populateGraphSettingFrame(self):
		self.hideAllWidgetsInFrame(self.graphSettingFrame)
		selectIndexTuple = self.graphSelectListbox.curselection()
		if selectIndexTuple:
			graphType = self.graphSelectListbox.get(selectIndexTuple).lower()
			graphClass = graphTypeClassMap.get(graphType,'NotInMap')

			self.titleLabel["text"] = self.graphSelectListbox.get(selectIndexTuple)
			self.titleLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0)

			if graphClass == "simple":
				self.nodeNumLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 1)
				self.nodeNumEntry.grid(in_ = self.graphSettingFrame, column = 1, row = 1)

			else:
				self.nodeNumLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 1)
				self.nodeNumEntry.grid(in_ = self.graphSettingFrame, column = 1, row = 1)
				self.label2.grid(in_ = self.graphSettingFrame, column = 0, row = 2)
				self.entry2.grid(in_ = self.graphSettingFrame, column = 1, row = 2)
		else:
			self.emptyLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0)
			

	def populateSimSettingFrame(self):
		self.hideAllWidgetsInFrame(self.simSettingFrame)
		self.numTrialLabel.grid(in_ = self.simSettingFrame, column = 0, row = 0)
		self.numTrialEntry.grid(in_ = self.simSettingFrame, column = 1, row = 0)
		self.startSimButton.grid(in_ = self.simSettingFrame, column = 0)

	#This is mostly to ignore the event for now, bit awkward
	def graphSettingSetup(self, event):
		self.populateGraphSettingFrame()

	def validateInputAndRunSim(self):
		try:
			numTrials = int(self.numTrialEntry.get())
			print(numTrials)
		except ValueError:
			print("Number of trials must be an integer")
		
root = tk.Tk()
root.resizable(width = False, height = False)
window = SimSettingWindow(root)
root.mainloop()
