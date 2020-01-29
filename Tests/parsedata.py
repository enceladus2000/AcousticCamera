'''
Parses delimited data from serial port and plots them continuously
the arduino should send serial data in the following format:

#waveform
23.34	232.3
32.44	2255.3
(etc)
#!waveform
'''

import numpy as np
import matplotlib.pyplot as plt 
import serial
import time
import sys

comport = "COM13"

#helper functions
def updatePlot():
	plt.clf()
	plt.plot(graph1, '-b')
	plt.plot(graph2, '-r')
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
		updatePlot()

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

#implement these into a class later?
graph1 = []
graph2 = []
graph_counter = 0
graph_maxcount = 600
waveform_collect = False

while True:
	#read a line from serial port and remove all trailing whitespace
	line = port.readline().strip()
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
			else:
				print("Error recognizing tailer " + data_tag)

		#lines starting with just '#' are headers
		else:
			data_tag = line[1:]		#extract the header name
			if data_tag == 'waveform':
				beginWaveformCollect()
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


print("Closing port...")
port.close()
