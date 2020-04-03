import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.ticker import StrMethodFormatter

c = 340		# speed of sound in m/s

# v simple sine wave omnidirectional non-attenuating source
class Source:
	def __init__(self, position, freq):
		self.position = position
		self.freq = freq

	def __repr__(self):
		return 'Source: pos = {p}, freq = {f}'.format(p=self.position, f=self.freq)

# omnidirectional mic class
class Mic:
	numSamples = 100		
	samplingRate = 5000		# sampling freq in Hz

	# position must be a tuple of length 2
	def __init__(self, position):
		self.position = position
		self.waveform = np.zeros(self.numSamples, dtype='float32')
		# t_range useful for generating waveform and plotting
		#self.t_range = np.linspace(0, self.numSamples / self.samplingRate, self.numSamples)

	# convenient for debugging
	def __repr__(self):
		return 'Mic: pos = {p}'.format(p=self.position)

	#func to generate wavefrom for different mics
	def generateWaveform(self, src):
		# calc phase difference
		phasediff = 2 * np.pi * src.freq * pointDist(src.position, self.position) / c

		# waveform will be sin(2(pi)vt + phi) 
		# where v is src.freq, t is the t_range
		t_range = np.linspace(0, self.numSamples / self.samplingRate, self.numSamples)
		self.waveform = np.sin(2*np.pi*src.freq*t_range - phasediff)	

# calculates abs distance btw two points represented as 2-tuples
def pointDist(p1, p2):
	dist = np.array(p1) - np.array(p2)
	dist = np.sqrt(dist.dot(dist))

	return dist

# calculates rms squared of waveform
def calcPower(waveform):
	return np.average(np.square(waveform))

# scanArea paramters
scanDistance = 50.0
numScanPoints = 31
scanLength = 50.0 
scanArea = [(x, scanDistance) for x in np.linspace(-scanLength/2, scanLength/2, numScanPoints)]
print('Scan Area: ', scanArea)

# initialise two mic objects in a linear arrangement on x axis
mic1 = Mic((-0.2, 0.0))
mic2 = Mic((0.2, 0.0))

# init a source somewhere in front of the mics
src = Source((-3.0, 5.5), 100.0)

# generate the mic's output waveform 
mic1.generateWaveform(src)
mic2.generateWaveform(src)

bfImage = []
# calculated phasediffs for each point - seems about right
phaseDiffs = []
for point in scanArea:
	# calculate delays
	d1 = pointDist(point, mic1.position) / c * mic1.samplingRate
	d2 = pointDist(point, mic2.position) / c * mic2.samplingRate
	phaseDiffs.append(360 * src.freq * (d1 - d2) / mic1.samplingRate )

	# 'zero' them
	min_d = min(d1, d2)
	d1 = int(round(d1 - min_d))
	d2 = int(round(d2 - min_d))
	print('rounded delays', (d1, d2))

	dnsSignal = mic1.waveform[d1:mic1.numSamples-d2] + mic2.waveform[d2:mic2.numSamples-d1]
	bfImage.append(calcPower(dnsSignal))

print('PhaseDiffs:', phaseDiffs)
# create x axis range
t_range = np.linspace(0, mic1.numSamples / mic1.samplingRate, mic1.numSamples)

# plot the generated waveforms
fig, axs = plt.subplots(2)

# plot raw mic waveforms in first subplot
axs[0].plot(t_range, mic1.waveform, color='blue', label='mic1')
axs[0].plot(t_range, mic2.waveform, color='red', label='mic2')

axs[0].grid(True)

axs[0].spines['left'].set_position('zero')
axs[0].spines['bottom'].set_position('center')
axs[0].spines['right'].set_color('none')
axs[0].spines['top'].set_color('none')

axs[0].xaxis.set_major_formatter(StrMethodFormatter('{x:,.3f}'))
axs[0].set_xticks(np.linspace(0, max(t_range), 4))
axs[0].set_yticks(np.linspace(*axs[0].get_ylim(), 5), 2)

axs[0].legend(loc='upper right')

# plot bfImage in 2nd subplot
axs[1].plot(bfImage)

plt.show()