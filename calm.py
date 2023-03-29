import RPi.GPIO as GPIO
import pywemo
import sys
from datetime import datetime
import time
import csv
import serial
import pygame
import smtplib 
from threading import Timer
import sys


print("hello world")

MicPin = 3
LedPin = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(MicPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LedPin, GPIO.OUT, initial=GPIO.LOW)
iCnt=0
action=0
threshold=0
lastruntime=None
nowruntime=None
mydevices=[]


#url = pywemo.setup_url_for_address("10.0.0.2")
#print(url)
#devices = pywemo.discover_devices()
#print(devices)
#print("current switch status:")
#print(devices[0].get_state())

with open('config.csv', encoding="utf8") as f:
    discdevices = pywemo.discover_devices()
    seldevices=[]
    csv_reader = csv.reader(f)
    for line in csv_reader:
        print("line:",line)
        print("name:",line[0])
        print("selected:",line[1])
        if line[1]=='1':
            seldevices.append(line[0])
    print("selected devices:",seldevices)    
    for device in discdevices:
        print("disc devices:",str(device))
        print("disc devices:",type(device))  
        if (str(device) in seldevices):
            print("device:",device)
            print("device status:",device.get_state())
            mydevices.append(device)
    for device in mydevices:
        print("my devices that are enabled:"+str(device))        

def send_email(subject, msg):
    try:
        print("email here", subject, msg)
        server = smtplib.SMTP('smtp.gmail.com:587')
        print(server)
        server.ehlo()
        server.starttls()
        server.login("c***@gmail.com", "***")
        print("email logged in")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        print(message)
        server.sendmail("c***@gmail.com", "h***@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")
        e = sys.exc_info()[0]
        print(e)
        

def takeAction():
    global action
    global iCnt
    global mydevices
    action=1
    global strdevices
    strdevices=""
    for device in mydevices:
        print("my devices that are enabled:"+str(device))
        strdevices+=str(device)
        strdevices+=","
    for device in mydevices:
        print("device before:",device.get_state())
        device.on()
        print("device after:", device.get_state())
    send_email("Calmspace: Sensory Room Activated",strdevices)
    
def my1(channel):
    global iCnt
    global threshold
    global lastruntime
    global nowruntime
    global action
    print("Sensor Triggered-->", time.ctime())
    
    nowruntime = datetime.now() # store current time
    
    if not lastruntime:
        print("Setting last run time to current time:")
        lastruntime = nowruntime
        iCnt=1
        action=0
    elif ((nowruntime - lastruntime).total_seconds()) > 30:
        print("Ignore prior last run. Reset to current time:")
        lastruntime = nowruntime
        iCnt=0
        action=0
    else:
        iCnt = iCnt +1
        print("Increment the counter to ", iCnt, "and action = ", action)
        if(iCnt > threshold and action==0):
            takeAction()
    print("<--")
    
GPIO.add_event_detect(MicPin, GPIO.RISING, callback=my1, bouncetime=200)

    
while True:
    pass
