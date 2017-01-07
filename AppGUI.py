import tkinter as tk
from tkinter import ttk

class AppGUI:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master, width = 640, height = 480, relief = tk.SUNKEN, bd = 30)
		self.frame.pack()

class SimSettingWindow:
	def __init__(self, master):
		self.master = master

		#Set up frames
		self.graphSelectFrame = tk.Frame(self.master)
		self.graphSelectFrame.grid(column = 0, row = 0)
		self.graphSettingFrame = tk.ttk.LabelFrame(self.master)
		self.graphSettingFrame.grid(column = 1, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)
		self.simSettingFrame = tk.ttk.LabelFrame(self.master)
		self.simSettingFrame.grid(column = 2, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)

		self.createWidgets()

		self.populateGraphSelectFrame()

		self.populateGraphSettingFrame(None)		
		self.populateGraphSelectListbox()
		
		self.populateSimSettingFrame(None)

	#Create all widgets
	def createWidgets(self):
		#---------------- graphSettingFrame widgets------------------
		self.emptyLabel = tk.Label(self.graphSettingFrame, text = "Select a graph type")

		self.nodeNumLabel = tk.Label(self.graphSettingFrame, text = "Number of nodes:")
		self.nodeNumEntry = tk.Entry(self.graphSettingFrame)

		self.label2 = tk.Label(self.graphSettingFrame, text = "Something else:")

		self.entry2 = tk.Entry(self.graphSettingFrame)
		#self.entry2.bind("a",self.qwe)

		#---------------- graphSelectFrame widgets ------------------
		self.graphSelectScrollbar = tk.ttk.Scrollbar(self.graphSelectFrame)
		self.graphSelectListbox = tk.Listbox(self.graphSelectFrame, yscrollcommand = self.graphSelectScrollbar.set, selectmode = tk.SINGLE)
		self.graphSelectListbox.bind("<Button-1>",self.graphSettingSetup)
		self.graphSelectScrollbar.config(command=self.graphSelectListbox.yview)

		#---------------- simSettingFrame widgets  ------------------
		self.numTrialLabel = tk.Label(self.simSettingFrame, text = "Number of trials:")

	def hideAllWidgetsInFrame(self, frame):
		for child in frame.winfo_children():
			child.grid_forget()

	def populateGraphSelectFrame(self):
		self.hideAllWidgetsInFrame(self.graphSelectFrame)
		self.graphSelectScrollbar.grid(column = 1, row = 0, sticky = tk.N + tk.S)
		self.graphSelectListbox.grid(column = 0, row = 0, sticky = tk.W, padx = 3, pady = 1)

	def populateGraphSelectListbox(self):
		if self.graphSelectListbox is not None:
			for item in ["one", "two", "three", "four",1,2,3,4,5,6,7,8]:
			    self.graphSelectListbox.insert(tk.END, item)
		else:
			print("Tried to populate graphListbox before it exists in SimSettingWindow")

	def populateGraphSettingFrame(self, graphType):
		self.hideAllWidgetsInFrame(self.graphSettingFrame)
		if graphType == None:
			self.emptyLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0)
		else:
			self.nodeNumLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0)
			self.nodeNumEntry.grid(in_ = self.graphSettingFrame, column = 1, row = 0)
			self.label2.grid(in_ = self.graphSettingFrame, column = 0, row = 1)
			self.entry2.grid(in_ = self.graphSettingFrame, column = 1, row = 1)

	def populateSimSettingFrame(self,something):
		self.hideAllWidgetsInFrame(self.simSettingFrame)
		self.numTrialLabel.grid(in_ = self.simSettingFrame, column = 2, row = 0)

	def graphSettingSetup(self, event):
		self.populateGraphSettingFrame("a")
root = tk.Tk()
window = SimSettingWindow(root)
root.mainloop()
