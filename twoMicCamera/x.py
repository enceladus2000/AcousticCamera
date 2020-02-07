str = input()
x = []
try:
	x.append(float(str))
	x.append(23.22)
except:
	print("can't")

print(x)
