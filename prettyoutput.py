#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

d = {1:12, 2:3, 4:5, 5:1, 6:10, 10:24, 11:15, 15:1, 20:15}


def freqHistogram(frequencyDict):
	maxIterKey = max(frequencyDict.keys())
	maxIterValue = max(frequencyDict.values())

	sortIter = sorted(frequencyDict)

	paddedIter = [0 for i in range(maxIterKey + 1)]

	for k,v in frequencyDict.items():
		paddedIter[k] = v

	fig, ax = plt.subplots()

	plt.bar(range(len(paddedIter)), paddedIter, align="center", facecolor = "green", alpha = 0.8)

	plt.xticks(range(len(paddedIter)), [i for i in range(len(paddedIter))])

	plt.xlabel("Iterations")
	plt.ylabel("Frequency")
	plt.title("Number of iterations until fixation")
	
	plt.xlim([-1, maxIterKey + 1])

	plt.show()
