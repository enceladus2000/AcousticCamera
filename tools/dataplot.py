'''
Simple program to plot two columns of float values coming from
the serial port and plot it on two graphs. Non numeric values
are printed on the serial port

The end goal is to be a more powerful and customized alternative
to the arduino IDE's serial monitor
'''

import numpy as np
import matplotlib.pyplot as plt 
import serial
import time
import sys

comport = "COM13"
numLines = 500

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

counter = 0
data = np.zeros((2, numLines), dtype='float32')
xaxis = [x for x in range(0, numLines)]

while True:
	#read a line from serial port and remove all trailing whitespace
	line = port.readline().strip()
	#convert from type bytes to type str
	line = line.decode('ascii')
	
	print(str(counter) + ": " + line)

	if len(line) == 0:
		continue
	#if line does have have numeric data, it most prolly starts with a non digit
	elif not line[0].isdigit():
		print(line)
	else:
		values = line.split('\t')
		if len(values) == 2:
			data[0][counter] = float(values[0])
			data[1][counter] = float(values[1])
			counter += 1
		else:
			print("Unexpected data: ", end='')
			print(values)
	if counter >= numLines:
		print('Plotting data...')
		counter = 0
		plt.clf()
		plt.plot(xaxis, data[0], '-r')
		plt.plot(xaxis, data[1], '-b')
		plt.draw()
		plt.pause(0.001)


print("Closing port...")
port.close()



