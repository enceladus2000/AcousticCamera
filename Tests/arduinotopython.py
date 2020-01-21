#code for taking sensor values from arduino using pyserial
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from time import sleep
ser=serial.Serial('/dev/ttyACM0', baudrate=115200)
ser.flushInput()
s1=[]                                            # empty list to store the data of sensor 1
s2=[]                                               # empty list to store the data of sensor 2
b=""
a=[]
s=""
data =[]   
n=int(input("Enter the no.of values to take at a time")  
n=100                
for i in range(n):
	b = ser.readline()         # read a byte string
	string_n = b[0:len(b)-2].decode("utf-8")  # decode byte string into Unicode  
	s = string_n.rstrip()
	a=s.split("    ")
	if(i>10):                            # leaving first few values to reduce error and garbage
		s1.append(float(a[0]))
		s2.append(float(a[1]))

ser.close()
print(s1)
print(s2)
c= [x for x in range(0,len(s1))]
plt.plot(c,s1)                               	#plotting values of sensor against natural no.
plt.plot(c,s2)
plt.show()
      # add to the end of data list
         # wait (sleep) 0.1 seconds


















