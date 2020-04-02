import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.ticker import StrMethodFormatter

c = 340		# speed of sound in m/s

# source class
	# list (not tuple, or singleton Sources) of Sources.
	# position - tuple, because not much 
	# frequency
	# __repr__
# mic class - includes sound sampling
	# position
	# generate waveform
	# waveform - numpy.array is better for a ton of calcs
	# __repr__ 

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
		# calculate distance between mic and source
		dist = np.array(src.position) - np.array(self.position)
		dist = np.sqrt(dist.dot(dist))
		# calc phase difference
		phasediff = 2 * np.pi * src.freq * dist / c

		print(str(self), ': phasediff =', phasediff)

		# waveform will be sin(2(pi)vt + phi) 
		# where v is src.freq, t is the t_range
		t_range = np.linspace(0, self.numSamples / self.samplingRate, self.numSamples)
		self.waveform = np.sin(2*np.pi*src.freq*t_range - phasediff)

# initialise two mic objects in a linear arrangement on x axis
mic1 = Mic((-2.0, 0.0))
mic2 = Mic((2.0, 0.0))

# init a source somewhere in front of the mics
src = Source((2.0, 2.0), 100.0)

# generate the mic's output waveform 
mic1.generateWaveform(src)
mic2.generateWaveform(src)

# create x axis range
t_range = np.linspace(0, mic1.numSamples / mic1.samplingRate, mic1.numSamples)

# plot the generated waveforms
fig, axs = plt.subplots(1)
axs.plot(t_range, mic1.waveform, color='blue', label='mic1')
axs.plot(t_range, mic2.waveform, color='red', label='mic2')

axs.grid(True)

axs.spines['left'].set_position('zero')
axs.spines['bottom'].set_position('center')
axs.spines['right'].set_color('none')
axs.spines['top'].set_color('none')

axs.xaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
axs.set_xticks(np.linspace(0, max(t_range), 4))
axs.set_yticks(np.linspace(*axs.get_ylim(), 5), 2)


axs.legend(loc='upper right')
plt.show()

# add all mics' waveforms together and get resultant power

# repeat these steps for different source positions

# and plot a graph of the resultant power for each position'''
