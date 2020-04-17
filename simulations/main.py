import acousticsim as acsim 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

showHeatmap = True

# initialise a linear 'scan area' that is
# distance away from origin, centered on y axis and parallel to x axis
scanArea = acsim.ScanArea(distance=50.0, length=50.0, numPoints=31)

# init a sound source of 100Hz
src = acsim.Source((20, scanArea.distance), 100.0)

# init mic array
micarray = acsim.MicArray(1.0, 2)

# generate waveforms for each mic
micarray.generateWaveforms(src)

bfImage = []		# contains beamformed acoustic 'image'
phaseDiffs = []		# calculated phasediffs for each point - seems about right

# simple delay and sum algorithm that calculates the
# sound intensity of each point in scanArea
for point in scanArea:
	# calculate delays
	delays = []
	for mic in micarray:
		delay = acsim.pointDist(point, mic.position) / acsim.c * micarray.samplingRate 
		delays.append(delay)

	# 'zero' them
	min_delay = min(delays)
	delays = np.array(delays) - min_delay

	# round delays[] to an int array
	delays = np.round(delays).astype(int)
	# print('delays at point', point, ' is:', delays)

	newSampleSize = micarray.sampleSize - max(delays)
	dnsSignal = np.zeros(newSampleSize)

	# add up shifted waveforms from each mic
	# how to get iterator?
	for i in range(micarray.arraySize):
		dnsSignal += micarray[i].waveform[ delays[i] : delays[i]+newSampleSize ]

	bfImage.append(acsim.calcPower(dnsSignal))

# create x axis range
t_range = np.linspace(0, micarray.sampleSize /micarray.samplingRate, micarray.sampleSize)

# plot the generated waveforms
fig, axs = plt.subplots(3)
# plot raw mic waveforms in first subplot
for mic in micarray:
	axs[0].plot(t_range, mic.waveform)
	plt.draw()
	plt.pause(0.001)

axs[0].grid(True)

axs[0].spines['left'].set_position('zero')
axs[0].spines['bottom'].set_position('center')
axs[0].spines['right'].set_color('none')
axs[0].spines['top'].set_color('none')

axs[0].xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}'))
axs[0].set_xticks(np.linspace(0, max(t_range), 4))
axs[0].set_yticks(np.linspace(*axs[0].get_ylim(), 5), 2)

# plot bfImage in 2nd subplot
axs[1].plot(bfImage)

# plot bfImage as a heatmap
# plt.rcParams["figure.figsize"] = 5,2
if showHeatmap is True:
	x = np.linspace(0, 1, len(bfImage))
	y = np.array(bfImage)
	extent = [(x[0]-(x[1]-x[0])/2), (x[-1]+(x[1]-x[0])/2), 0, 1]

	axs[2].imshow(y[np.newaxis,:], cmap="plasma", aspect="auto", extent=extent)
	axs[2].set_yticks([])	# no y ticks
	axs[2].set_xlim(extent[0], extent[1])
	plt.tight_layout()
else:
	axs[2].set_axis_off()

plt.show()
