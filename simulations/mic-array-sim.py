import numpy as np
import matplotlib.pyplot as plt 
# omnidirectional mic class, limited to 2 dimension for now 
class Mic:
	numSamples = 100
	# position must be a tuple of length 2
	def __init__(self, position):
		self.position = position
		self.waveform = np.zeros(self.numSamples, dtype='float32')
	#func to generate wavefrom for different mics
	def generateWaveform1(self):
		global wavef1,wavef2,t
		t=np.linspace(-np.pi,np.pi,256)
		wavef1=np.sin(t)
		wavef2=np.cos(t)
		Mic.plotwaveform()
	def plotwaveform():		#to plot the data from different mics
		fig,ax=plt.subplots(2)
		ax[0].plot(t,wavef1)
		ax[0].set_xlabel("Data from mic1")
		ax[1].plot(t,wavef2)
		ax[1].set_xlabel("Data from mic2")
		plt.show()
# simple sine wave omnidirectional source
class Source:
	def __init__(self, position, freq):
		self.position = position
		self.freq = freq

# initialise two mic objects in a linear array
mic1 = Mic((2.0,0.0))
mic2 = Mic((-2.0,0.0))
src = Source((3.0,2.0),100.0)
# init a source somewhere in front of the mics
fig,axs=plt.subplots(2)
# generate the mic's output waveform (Mic.generateWaveform())

mic1.generateWaveform1()
mic2.generateWaveform2()
# plot them
    
# add all mics' waveforms together and get resultant power

# repeat these steps for different source positions

# and plot a graph of the resultant power for each position'''
