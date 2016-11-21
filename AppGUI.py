import tkinter as tk
from tkinter import ttk

class AppGUI:
	def __init__(self, master):
		self.master = master
		self.frame = tk.Frame(self.master, width = 640, height = 480, relief = tk.SUNKEN, bd = 30)
		self.but1 = tk.Button(self.frame, text = "blah")
		self.but1.pack()
		self.frame.pack()

class SimSettingWindow:
	def __init__(self, master):
		self.master = master

		self.graphSelectFrame = tk.Frame(self.master)
		self.graphSelectFrame.grid(column = 0, row = 0)
		self.graphListboxScrollbar = tk.ttk.Scrollbar(self.graphSelectFrame)
		self.graphListboxScrollbar.grid(column = 1, row = 0, sticky = tk.N + tk.S)
		self.graphListbox = tk.Listbox(self.graphSelectFrame, yscrollcommand = self.graphListboxScrollbar.set, selectmode = tk.SINGLE)
		self.populateListbox()
		self.graphListbox.grid(column = 0, row = 0, sticky = tk.W, padx = 3, pady = 1)
		self.graphListboxScrollbar.config(command=self.graphListbox.yview)

		self.graphSettingFrame = tk.ttk.LabelFrame(self.master)
		self.graphSettingFrame.grid(column = 1, row = 0, sticky = tk.N + tk.E + tk.S + tk.W)
		self.nodeNumLabel = tk.Label(self.graphSettingFrame, text = "Number of nodes:")
		self.nodeNumLabel.grid(in_ = self.graphSettingFrame, column = 0, row = 0)
		self.nodeNumEntry = tk.Entry(self.graphSettingFrame)
		self.nodeNumEntry.grid(in_ = self.graphSettingFrame, column = 1, row = 0)
		self.label2 = tk.Label(self.graphSettingFrame, text = "Something else:")
		self.label2.grid(in_ = self.graphSettingFrame, column = 0, row = 1)
		self.entry2 = tk.Entry(self.graphSettingFrame)
		self.entry2.grid(in_ = self.graphSettingFrame, column = 1, row = 1)

		self.simSettingFrame = tk.ttk.LabelFrame(self.master)
		self.simSettingFrame.grid(column = 2, row = 0)

	def populateListbox(self):
		if self.graphListbox is not None:
			for item in ["one", "two", "three", "four",1,2,3,4,5,6,7,8]:
			    self.graphListbox.insert(tk.END, item)
		else:
			print("Tried to populate graphListbox before it exists in SimSettingWindow")

root = tk.Tk()
window = SimSettingWindow(root)
root.mainloop()
