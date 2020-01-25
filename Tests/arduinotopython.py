#code for taking sensor values from arduino using pyserial
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from time import sleep
try:
	ser=serial.Serial('/dev/ttyACM0', baudrate=115200,timeout=1)
except:
	print("port not found")
time.sleep(2)
ser.flushInput()
s1=[]                                            # empty list to store the data of sensor 1
s2=[]                                               # empty list to store the data of sensor 2
a=[]
s=""
data =[]    
n=500              
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
fig,ax=plt.subplots()
line=ax.plo(y_var)
plt.subplot(c,s1,'ro')                               #plotting values of sensor against natural no.
plt.subplot(c,s2)
plt.ylabel("sensor values")
plt.suptitle("values of both the sensors")
plt.show()
      # add to the end of data list
         # wait (sleep) 0.1 seconds


















