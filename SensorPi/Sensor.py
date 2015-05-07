import time
import picamera
import os
import glob
import datetime

#imports for sending
from socket import *



base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def camera():
    cam = picamera.PiCamera()
    #cam.resolution(1024, 768)
    cam.start_preview()
    time.sleep(2)
    cam.capture('test.jpg')

	#CHECK TEMPRATURE
def read_temp_raw():
	f= open(device_file, 'r')
	lines= f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	log_entry=st+" "+str(temp_c)
	return [log_entry, str(temp_c)]
	
def temp():
	os.system('sudo modprobe w1-gpio')  #Needed for RPi model B
	os.system('sudo modprobe w1-therm') #Needed for RPi model B
	
	ts1=time.time()
	temp_log_entry=read_temp()
	f = open('TempLog.txt','a')
	g = open('TempLastValue.txt','w')
	f.write(temp_log_entry[0]+"\n")
	g.write(temp_log_entry[0]+"\n")
	g.close()
	f.close()
	ts2=time.time()
	delay=1.0-(ts2-ts1)
	time.sleep(delay)
	return temp_log_entry[1]

	#SOCKET function
def sendToServer():
	host = "213.159.191.221"
	port = 50010
	s = socket(AF_INET, SOCK_STREAM)
	s.connect((host,port))
	print ("Socket connected") #Currently not working
	f = open('test.jpg','rb')
	print ('Sending...')
	l = f.read(1024)
	while (l):
		print ('Sending...')
		s.send(l)
		l = f.read(1024)
	f.close()
	print ("Done Sending")
	#print s.recv(1024)
	s.close                 
	
	
#MAIN function
while True:
	time.sleep(10)
	temprature = float (temp())
	print(temprature)
	camera()
	sendToServer()		
		
		
		
