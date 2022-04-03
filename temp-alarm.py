# coding=utf-8

import sys, time, re

targetTemp  = float(sys.argv[1])
device = sys.argv[2]

devicePath = '/sys/bus/w1/devices/'+device+'/w1_slave' 

def main():
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

while True:
    main()
    time.sleep(1)
