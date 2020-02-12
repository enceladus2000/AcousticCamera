import numpy as np

# omnidirectional mic class, limited to 2 dimension for now 
class Mic:
	numSamples = 100

	# position must be a tuple of length 2
	def __init__(self, position):
		self.position = position
		self.waveform = np.zeros(self.numSamples, dtype='float32')

# simple sine wave omnidirectional source
class Source:
	def __init__(self, position, freq):
		self.position = position
		self.freq = freq

# initialise two mic objects in a linear array

# init a source somewhere in front of the mics

# generate the mic's output waveform (Mic.generateWaveform())

# plot them

# add all mics' waveforms together and get resultant power

# repeat these steps for different source positions

# and plot a graph of the resultant power for each position
