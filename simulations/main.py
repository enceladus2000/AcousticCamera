import acousticsim as acsim 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

# scanArea paramters
scanDistance = 50.0
numScanPoints = 31
scanLength = 50.0 
scanArea = [(x, scanDistance) for x in np.linspace(-scanLength/2, scanLength/2, numScanPoints)]
print('Scan Area: ', scanArea)

# init mic array
mics = []
numMics = 2

for x in np.linspace(-0.2, 0.2, numMics):
	mics.append(acsim.Mic((x, 0)))

for mic in mics:
	print(mic)

# init a source somewhere in front of the mics
src = acsim.Source((20, scanDistance), 100.0)

# generate the mics' output waveform 
for mic in mics:
	mic.generateWaveform(src)

bfImage = []		# contains beamformed acoustic 'image'
phaseDiffs = []		# calculated phasediffs for each point - seems about right

# calculate intensity of each point in scanArea and append to bfImage
for point in scanArea:
	# calculate delays
	delays = []
	for mic in mics:
		delay = acsim.pointDist(point, mic.position) / acsim.c * acsim.micSamplingRate
		delays.append(delay)

	# 'zero' them
	min_delay = min(delays)
	delays = np.array(delays) - min_delay

	# round delays[] to an int array
	delays = np.round(delays).astype(int)
	print('delays at point', point, ' is:', delays)

	newSampleSize = acsim.micSampleSize - max(delays)
	dnsSignal = np.zeros(newSampleSize)

	# how to get iterator?
	for i in range(numMics):
		dnsSignal += mics[i].waveform[ delays[i] : delays[i]+newSampleSize ]

	bfImage.append(acsim.calcPower(dnsSignal))

# create x axis range
t_range = np.linspace(0, acsim.micSampleSize / acsim.micSamplingRate, acsim.micSampleSize)

# plot the generated waveforms
fig, axs = plt.subplots(2)

# plot raw mic waveforms in first subplot
for mic in mics:
	axs[0].plot(t_range, mic.waveform)

axs[0].grid(True)

axs[0].spines['left'].set_position('zero')
axs[0].spines['bottom'].set_position('center')
axs[0].spines['right'].set_color('none')
axs[0].spines['top'].set_color('none')

axs[0].xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}'))
axs[0].set_xticks(np.linspace(0, max(t_range), 4))
axs[0].set_yticks(np.linspace(*axs[0].get_ylim(), 5), 2)

# axs[0].legend(loc='upper right')

# plot bfImage in 2nd subplot
axs[1].plot(bfImage)

plt.show()