import numpy as np

c = 340		# speed of sound in m/s

micSamplingRate = 5000
micSampleSize = 100

# simple sine wave source (non attenuating)
class Source:
	def __init__(self, position, freq):
		self.position = position
		self.freq = freq

	def __repr__(self):
		return 'Source: pos = {p}, freq = {f}'.format(p=self.position, f=self.freq)

# simple omnidirectional mic
class Mic:
	# position must be a tuple of length 2
	def __init__(self, position):
		self.position = position
		self.waveform = np.zeros(micSampleSize, dtype='float32')
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
		t_range = np.linspace(0, micSampleSize / micSamplingRate, micSampleSize)
		self.waveform = np.sin(2*np.pi*src.freq*t_range - phasediff)	

def MicArray:
	samplingRate = 5000		# in Hz
	sampleSize = 100

	# initialise a uniform linear array of mics
	def __init__(self, length, numMics):
		mics = []
		arraySize = numMics

		for x in np.linspace(-length/2, length/2, arraySize):
			mics.append(Mic((x, 0)))

	def generateWaveforms(self):
		for mic in mics:
			mic.generateWaveform()



# calculates abs distance btw two points represented as 2-tuples
def pointDist(p1, p2):
	dist = np.array(p1) - np.array(p2)
	dist = np.sqrt(dist.dot(dist))

	return dist

# calculates rms squared of waveform
def calcPower(waveform):
	return np.average(np.square(waveform))