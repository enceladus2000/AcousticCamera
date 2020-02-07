'''
Parses delimited data from serial port and plots them continuously
the arduino should send serial data in the following format:

#waveform
23.34	232.3
32.44	2255.3
(etc)
#!waveform

#bfimage
34.23
(etc)
#!bfimage
'''

import numpy as np
import matplotlib.pyplot as plt 
import serial
import time
import sys

comport = "COM13"

#helper functions
def beginBFImageCollect():
	global bfi_collect, bfi_counter
	global bfidata

	bfi_collect = True
	bfi_counter = 0
	bfidata = []

def endBFImageCollect(plotredraw = True):
	global bfi_collect
	bfi_collect = False
	if plotredraw:
		plotBFI()

def plotBFI():
	axs[1].cla()
	axs[1].plot(bfidata)
	plt.draw()
	plt.pause(0.001)

def updateWaveformPlot():
	axs[0].cla()
	axs[0].plot(graph1, '-b')
	axs[0].plot(graph2, '-r')
	plt.draw()
	plt.pause(0.001)

def beginWaveformCollect():
	#declare them global to manipulate
	global waveform_collect, graph_counter
	global graph1, graph2

	waveform_collect = True
	#reset all related vars
	graph_counter = 0
	graph1 = []
	graph2 = []
	print("Received header waveform")

def endWaveformCollect(plotredraw = True):
	global waveform_collect
	waveform_collect = False
	if plotredraw:
		updateWaveformPlot()

#main code
try:
	port = serial.Serial(comport, baudrate=115200, timeout=1)
except:
	print("Port not found, exiting...");
	sys.exit();

print("Successfully opened serial port " + port.name)
port.flushInput()

#pyplot must be in interative mode to not block program when plotting
#these two lines init pyplot for that purpose
plt.ion()
plt.show()
fig, axs = plt.subplots(2)

#implement these into a class later?
graph1 = []
graph2 = []
graph_counter = 0
graph_maxcount = 700
waveform_collect = False

bfi_counter = 0
bfi_maxcount = 100
bfidata = []
bfi_collect = False

while True:
	#read a line from serial port and remove all trailing whitespace
	try:
		line = port.readline().strip()
	except:
		print("Serial port must have closed")
		sys.exit()

	#convert from type bytes to type str
	line = line.decode('ascii')

	#don't go ahead if empty string received
	if len(line) < 2:
		continue
	#code to recognize header/tailers
	elif line[0] == '#':
		#lines starting with '#!' are tailers
		if line[1] == '!':			#extract tailer name
			data_tag = line[2:]
			if data_tag == 'waveform':
				print("Stopping waveform collect at " + str(graph_counter))
				endWaveformCollect()
			elif data_tag == 'bfimage':
				print("Stopping bfidata collect at " + str(bfi_counter))
				endBFImageCollect()
			else:
				print("Error recognizing tailer " + data_tag)

		#lines starting with just '#' are headers
		else:
			data_tag = line[1:]		#extract the header name
			if data_tag == 'waveform':
				beginWaveformCollect()
			elif data_tag == 'bfimage':
				beginBFImageCollect()
			else:
				print("Error recognizing header " + data_tag)

	#now check if data is non-numeric and directly print that to cmd
	elif line[0].isdigit() == False:
		print(line)
	#collect waveform data
	elif waveform_collect == True:
		values = line.split('\t')
		if len(values) == 2:
			#print(values)
			#append data into lists
			graph1.append(float(values[0]))
			graph2.append(float(values[1]))

			graph_counter += 1
			if graph_counter >= graph_maxcount:
				print("Waveform max count reached, resetting...")
				endWaveformCollect()
		else:
			print("Unexpected numeric data : " + line)

	#collect bfi data
	elif bfi_collect == True:
		try:
			bfidata.append(float(line))
			bfi_counter += 1

			if bfi_counter >= bfi_maxcount:
				print("BFI data max count reached, resetting...")
				endBFImageCollect()
		except:
			print("Invalid BFI Data!")

print("Closing port...")
port.close()
