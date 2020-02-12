import numpy as np

class Mic:
	numSamples = 100
	
	def __init__(self, position):
		self.position = position
		self.waveform = np.zeros(self.numSamples, dtype='float32')
