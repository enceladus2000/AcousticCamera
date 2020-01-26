#code for taking sensor values from arduino using pyserial
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from time import sleep
import matplotlib.animation as animation

try:
	ser=serial.Serial('COM7', baudrate=115200,timeout=1)
except:
	print("port not found")
	
time.sleep(2)
ser.flushInput()
s1=[]                                            # empty list to store the data of sensor 1
s2=[]                                               # empty list to store the data of sensor 2
a=[]
s=""
<<<<<<< HEAD
data =[] 
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
print("hello")
def animate(i):    
	ax1.clear()            
	b = ser.readline()
	
	print(b)   
	try:
		string_n = b[0:len(b)-2].decode("utf-8")  # decode byte string into Unicode  
		s = string_n.rstrip()
		a=s.split("\t")
		print(a)                 # leaving first few values to reduce error an
		s1.append(float(a[0]))
		s2.append(float(a[1]))

		c= [x for x in range(0,500)]
	except:
		print(b)
		pass
	if(len(s1)>510):
			print("here")
			plt.plot(c,s1[-500:],'ro')                               #plotting values of sensor against nat
			plt.plot(c,s2[-500:])
			plt.ylabel("sensor values")
			plt.suptitle("values of both the sensors")
ani=animation.FuncAnimation(fig, animate, interval=100)
=======
data =[]    
n=500              
for i in range(n):
	b = ser.readline()         # read a byte string
	print(b)
	if (len(b) < 6):
		print("Invalid string received")
		break;
	string_n = b[0:len(b)-2].decode("utf-8")  # decode byte string into Unicode  
	s = string_n.rstrip()
	a=s.split("\t")
	print(a)
	if(i>10):                            # leaving first few values to reduce error and garbage
		s1.append(float(a[0]))
		s2.append(float(a[1]))

ser.close()
# print(s1)
# print(s2)
c= [x for x in range(0,len(s1))]
plt.plot(c,s1,'-r')                               #plotting values of sensor against natural no.
plt.plot(c,s2, '-b')
plt.ylabel("sensor values")
plt.suptitle("values of both the sensors")
>>>>>>> 9baf11456aa96f1604676be2a794e14e235fc730
plt.show()
	      # add to the end of data list
		 # wait (sleep) 0.1 seconds


















