import os
os.chdir('/home/pi/TempPhoto')
for filename in os.listdir(r'/home/pi/TempPhoto'):
	os.remove(filename)
