import numpy as np
import matplotlib.pyplot as plt
import serial
import time
from time import sleep
import matplotlib.animation as animation

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

# print(s1)
# print(s2)
c= [x for x in range(0,len(s1))]
plt.plot(c,s1)                               #plotting values of sensor against natural no.
plt.plot(c,s2 )
plt.ylabel("sensor values")
plt.suptitle("values of both the sensors")
plt.show()


















>>>>>>> 42d8015d37bcf41f4ffcff8457934318ef260dc2
