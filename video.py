import sys,os,picamera
import shutil
import re
from PIL import Image, ImageDraw ,ImageFont
from subprocess import *
import time
 
#設定字體
font = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf",50)
font0 = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf",120)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf",20)
font3 = ImageFont.truetype("/usr/share/fonts/truetype/droid/DroidSans.ttf",40)
counter = 1
counter123 = 0
Temtemp = 0
Humtemp = 0
Tumm = []
Humm = []
list1 = []
bunn = ""
os.chdir('/home/pi/TempPhoto')
 
#把資料夾的所有照片列舉出來
list1 = sorted(os.listdir(r'/home/pi/TempPhoto'))
list1.reverse()
 
#利用字母切割出時間與溫溼度後，存入矩陣
while (len(list1) != 0):
        file = list1.pop()
        if file.endswith('.jpg'):
                name = os.path.splitext(file)[0]
                name = re.split('T|H',name)
                Tem = float(name[1])
                Hum = float(name[2])
                Temtemp += Tem
                Humtemp += Hum
		
		#為了防止溫濕度跳動太大，我們取每個小時的平均值
                if counter123 < 19:
                        counter123 += 1
                else:
                        Tumm.append(round(Temtemp/20,1))
                        Tumm.append(round(Temtemp/20,1))
                        Humm.append(round(Humtemp/20,1))
                        Humm.append(round(Humtemp/20,1))
			Temtemp = 0
                        Humtemp = 0
                        counter123 = 0
                        
#這邊有設一個機制，防止照片有缺少時，也能成功取得平均溫濕度
if counter123 !=0:
        Tumm.append(round(Temtemp/counter123,1))
        Tumm.append(round(Temtemp/counter123,1))
        Humm.append(round(Humtemp/counter123,1))
        Humm.append(round(Humtemp/counter123,1))
 
#進行後製動作，打開照片後，利用剛才的矩陣資料處理
for file in sorted(os.listdir(r'/home/pi/TempPhoto')):
    if file.endswith('.jpg'):
        im = Image.open(file)
        draw = ImageDraw.Draw(im)
        timename = os.path.splitext(file)[0]
        timename = re.split(':|T',timename)
        tempbunn = int(timename[1])/15
        if tempbunn == 3:
                bunn = ":45"
        elif tempbunn == 1:
                bunn = ":15"
        elif tempbunn == 2:
                bunn = ":30"
        elif tempbunn == 0:
                bunn = ":00"
        draw.text((50,480),timename[0]+bunn,fill=(255,255,255),font=font0)
        draw.text((55,605),str(Tumm[int((counter-1)/20)])+' c',fill=(255,255,255),font=font)
        draw.text((217,605),str(Humm[int((counter-1)/20)]),fill=(255,255,255),font=font)
        draw.text((157,610),'o',fill=(255,255,255),font=font2)
        draw.text((317,615),'%',fill=(255,255,255),font=font3)
	
	#儲存照片，儲存兩張的原因是為了接下來的壓制影片需求
        im.save('image%03d.jpg' %(counter))
        counter += 1
        im.save('image%03d.jpg' %(counter))
        counter += 1
        
#這裡我們把每秒fps設定為15，搭配上面一次儲存兩張相同檔案，可以把影片長度拉長兩倍
call (['ffmpeg','-f','image2','-i','image%03d.jpg','-r','15','output.mp4'])
