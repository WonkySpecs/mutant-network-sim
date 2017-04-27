#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

def freqHistogram(frequencyDict):
	maxIterKey = max(frequencyDict.keys())
	maxIterValue = max(frequencyDict.values())
	minIterKey = min(frequencyDict.keys())

	keyDiff = maxIterKey - minIterKey

	sortIter = sorted(frequencyDict)

	paddedIter = [0 for i in range(minIterKey, maxIterKey + 1)]

	for k,v in frequencyDict.items():
		paddedIter[k - minIterKey] = v

	numElements = len(paddedIter)
	fig, ax = plt.subplots()

	plt.bar(range(minIterKey, maxIterKey + 1), paddedIter, align = "center", facecolor = "green", alpha = 0.8)

	plt.xlim([minIterKey - 3, maxIterKey + 3])

	plt.xticks(range(minIterKey, maxIterKey, numElements//20), [minIterKey + ((numElements//20) * i) for i in range(numElements)], rotation = 80)

	plt.xlabel("Iterations")
	plt.ylabel("Frequency")
	plt.title("Number of iterations until fixation")

	plt.show()
