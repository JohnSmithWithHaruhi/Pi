import sys
import os
import picamera
import shutil
from subprocess import *
from re import search
import time
 
def run_cmd(cmd):
	p = Popen(cmd, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output
	
def get_HT():
	#呼叫程式碼，並印出溫溼度
	output = run_cmd("sudo ./DHT_CharLCD/DHT 11 15")
	print output
	
	#利用Match把溫溼度抓出來
	matches = search("Temp =\s+([0-9.]+)", output)
	if (not matches):
		return 1
	global temp
	temp = float(matches.group(1))
	matches = search("Hum =\s+([0-9.]+)", output)
	if (not matches):
		return 1global humidity
	humidity = float(matches.group(1))
        		
while 1:
	#重複讀取溫溼度，如果失敗休息三秒在進行一次
	DHT_msg = get_HT()
	if(DHT_msg == 1):
		time.sleep(3)
		continue
	else:
		break
		
os.chdir("/home/pi/TempPhoto") #切換資料夾
camera = picamera.PiCamera()
camera.resolution = (1280,720) #設定影像解析度
camera.vflip = True #垂直翻轉
camera.hflip = True #水平翻轉
camera.start_preview()
time.sleep(3)
#拍照，設定檔名為時間、溫度和濕度的組合
camera.capture(time.strftime("%H:%M")+" T"+str(temp)+" H"+str(humidity)+'.jpg','jpeg')
