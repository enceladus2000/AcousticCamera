import numpy as np

c = 340		# speed of sound in m/s

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

	# convenient for debugging
	def __repr__(self):
		return 'Mic: pos = {p}'.format(p=self.position)

	#func to generate wavefrom wrt sound src
	def generateWaveform(self, src, samplingRate=5000, sampleSize=100):
		# calc phase from distance btw src and mic
		phasediff = 2 * np.pi * src.freq * pointDist(src.position, self.position) / c

		# waveform will be sin(2(pi)vt + phi) 
		# where v is src.freq, t is the t_range
		t_range = np.linspace(0, sampleSize / samplingRate, sampleSize)
		self.waveform = np.sin(2*np.pi*src.freq*t_range - phasediff)

# class containing array of Mic[]
class MicArray:
	samplingRate = 10000		# in Hz
	sampleSize = 100

	# initialise a uniform linear array of mics
	def __init__(self, length, numMics):
		self.mics = []
		self.arraySize = numMics

		for x in np.linspace(-length/2, length/2, self.arraySize):
			self.mics.append(Mic((x, 0)))

	# iterable, must be able to be iterated, eg: for mic in micarray
	def __iter__(self):
		self.i = 0
		return self

	def __next__(self):
		if self.i < self.arraySize:
			temp_mic = self.mics[self.i]
			self.i += 1
			return temp_mic
		else:
			raise StopIteration
	
	def __getitem__(self, index):
		return self.mics[index]
	
	def __len__(self):
		return self.arraySize

	# make all mics in array prepare waveforms
	def generateWaveforms(self, src):
		for mic in self.mics:
			mic.generateWaveform(src, self.samplingRate, self.sampleSize)

class ScanArea:
	# make linear scan area at scanDistance from origin
	# centered on y axis, parallel to x axis
	def __init__(self, distance, length, numPoints):
		self.distance = distance
		self.length = length
		self.numPoints = numPoints
		self.scanArea = [(x, distance) for x in np.linspace(-length/2, length/2, numPoints)]


	# configure as iterable object
	def __getitem__(self, index):
		return self.scanArea[index]

	def __iter__(self):
		self.point_i = 0
		return self

	def __next__(self):
		if self.point_i < self.numPoints:
			point = self.scanArea[self.point_i]
			self.point_i += 1
			return point
		else:
			raise StopIteration

# calculates abs distance btw two points represented as tuples
# works for 2D and 3D coordinates
def pointDist(p1, p2):
	dist = np.array(p1) - np.array(p2)
	dist = np.sqrt(dist.dot(dist))

	return dist

# calculates rms squared of waveform
def calcPower(waveform):
	return np.average(np.square(waveform))