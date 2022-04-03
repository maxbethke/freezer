# coding=utf-8

import sys, time, re, os
import RPi.GPIO as GPIO
from dotenv import load_dotenv
import requests, random

targetTemp  = float(sys.argv[1])
device = sys.argv[2]

devicePath = '/sys/bus/w1/devices/'+device+'/w1_slave' 
buzzerPin = 17
wasLastTempOk = True

textsTempOk = [
    'Okay, wir haben wieder ein gemütliches Level von TEMP% Grad erreicht \xF0\x9F\x98\x8E',
    'Ah, so ists viel besser. Mein Themometer misst wieder %TEMP% Grad.',
    'Alles wieder cool hier. Ich messe %TEMP% Grad.'
    ]
textsTempNotOk = [
    'Hier wirds langsam ungemütlich... %TEMP% Grad and rising \xE2\x9A\xA0',
    'Irgendwas läuft heir schief... ich bin schon wieder bei %TEMP% Grad \xF0\x9F\x94\xA5',
    'Ich schmelzeeee \xF0\x9F\x92\xA6'
    ]

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)
buzzer = GPIO.PWM(buzzerPin, 800)

load_dotenv()

def main():
    global wasLastTempOk

    temp = getTemperature()

    if temp is None:
        print('Can not get temperature')
        return

    isTempOk = temp <= targetTemp
    
    print(
         time.strftime("%x %X"),
         'Temperature: ',
         temp,
         'C ',
         ('HI', 'OK')[isTempOk]
    )

    if isTempOk:
        buzzer.stop()
    else:
        buzzer.start(50)

    if isTempOk != wasLastTempOk:
        messageText = getMessageText(isTempOk, temp)
        sendTelegramMessage(messageText)

    wasLastTempOk = isTempOk
def getTemperature():
    for i in range(3):
        temp = readSensor()
        if isinstance(temp, float):
            return temp
        time.sleep(1)
        print('Didnt get temp, retrying')
    print(time.strftime("%x %X"), temp)

def readSensor(path=devicePath):
    value = 'No temperature was read'
    try:
        f = open(path, "r")
        line = f.readline()
        while line == '':
            f.close()
            time.sleep(0.5)
            f = open(path, 'r')
            line = f.readline()
        if not re.match("([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
            f.close()
            return path
            #return 'Invalid temperature was read'
        line = f.readline()
        m = re.match("([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
        if m:
            value = float(m.group(2)) / 1000.0
    except IOError as e:
        value = "Error reading "+path+": "+e
    f.close()
    return value

def getMessageText(isTempOk, temp):
    if isTempOk:
        text = random.choice(textsTempOk)
    else:
        text = random.choice(textsTempNotOk)
    return text.replace('%TEMP%', str(temp))

def sendTelegramMessage(message):
    url = 'https://api.telegram.org/bot'+os.getenv('TELEGRAM_BOT_TOKEN')+'/sendMessage'

    params = {
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'parse_mode': 'Markdown',
        'text': message
    }

    res = requests.get(url, params=params)
    print(res.url)
    print('Send Telegram Message', res)
while True:
    main()
    time.sleep(1)
