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
