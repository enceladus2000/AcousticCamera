import numpy as np
import matplotlib.pyplot as plt 

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
	samplingRate = 1000		# sampling freq in Hz

	# position must be a tuple of length 2
	def __init__(self, position):
		self.position = position
		self.waveform = np.zeros(self.numSamples, dtype='float32')
		# t_range useful for generating waveform and plotting
		self.t_range = np.linspace(0, self.numSamples / self.samplingRate, self.numSamples)


	#func to generate wavefrom for different mics
	def generateWaveform(self, src):
		# calculate distance between mic and source
		dist = np.array(src.position) - np.array(self.position)
		dist = np.sqrt(dist.dot(dist))
		# calc phase difference
		phasediff = 2 * np.pi * src.freq * dist / c

		# waveform will be sin(2(pi)vt + phi) 
		# where v is src.freq
		self.waveform = np.sin(2*np.pi*src.freq*self.t_range + phasediff)

	# def plotwaveform():		#to plot the data from different mics
	# 	fig,ax=plt.subplots(2)
		# ax[0].plot(t,wavef1)
		# ax[0].set_xlabel("Data from mic1")
		# ax[1].plot(t,wavef2)
		# ax[1].set_xlabel("Data from mic2")
		# plt.show()

# initialise two mic objects in a linear arrangement on x axis
mic1 = Mic((2.0, 0.0))
mic2 = Mic((-2.0, 0.0))

# init a source somewhere in front of the mics
src = Source((0, 2.0), 100.0)

# generate the mic's output waveform 
mic1.generateWaveform(src)
mic2.generateWaveform(src)

# plot them
fig, axs = plt.subplots(2)
axs[0].plot(mic1.t_range, mic1.waveform)
axs[0].set_ylabel("Data from mic1")
axs[1].plot(mic2.t_range, mic2.waveform)
axs[1].set_ylabel("Data from mic2")
plt.show()

# add all mics' waveforms together and get resultant power

# repeat these steps for different source positions

# and plot a graph of the resultant power for each position'''
