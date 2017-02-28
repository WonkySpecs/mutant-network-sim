#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

def freqHistogram(frequencyDict):
	maxIterKey = max(frequencyDict.keys())
	maxIterValue = max(frequencyDict.values())

	sortIter = sorted(frequencyDict)

	paddedIter = [0 for i in range(maxIterKey + 1)]

	for k,v in frequencyDict.items():
		paddedIter[k] = v

	numElements = len(paddedIter)
	fig, ax = plt.subplots()

	plt.bar(range(numElements), paddedIter, align="center", facecolor = "green", alpha = 0.8)

	plt.xticks(range(0, numElements, numElements//20), [(numElements//20) * i for i in range(numElements)])

	plt.xlabel("Iterations")
	plt.ylabel("Frequency")
	plt.title("Number of iterations until fixation/extinction")
	
	plt.xlim([-1, maxIterKey + 1])

	plt.show()
