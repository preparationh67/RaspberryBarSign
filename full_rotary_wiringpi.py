#!/usr/bin/env python
import wiringpi as wpi
import datetime


pCLK = 3
pDT = 4
pSW = 5

globalCounter = 24
flag = 0
Last_DT_Status = 0
Current_DT_Status = 0
LastClearTime = 0


def setup():
    wpi.wiringPiSetup()
    wpi.pinMode(pCLK, wpi.INPUT)
    wpi.pinMode(pDT, wpi.INPUT)
    wpi.pinMode(pSW, wpi.INPUT)
    wpi.pullUpDnControl(pSW, wpi.PUD_UP)
    rotaryClear()


def rotaryDeal():
    global flag
    global Last_DT_Status
    global Current_DT_Status
    global globalCounter
    # Last_DT_Status = GPIO.input(pDT)
    Last_DT_Status = wpi.digitalRead(pDT)
    while (not wpi.digitalRead(pCLK)):
        Current_DT_Status = wpi.digitalRead(pDT)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_DT_Status == 0) and (Current_DT_Status == 1):
            globalCounter = globalCounter + 1
            print 'globalCounter = %d' % globalCounter
        if (Last_DT_Status == 1) and (Current_DT_Status == 0):
            globalCounter = globalCounter - 1
            print 'globalCounter = %d' % globalCounter


def clear(ev=None):
    global LastClearTime
    if LastClearTime == 0 or (datetime.datetime.now() - LastClearTime) > datetime.timedelta(seconds=1):
        globalCounter = 0
        print 'globalCounter = %d' % globalCounter
        LastClearTime = datetime.datetime.now()


def rotaryClear():
    # GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling
    wpi.wiringPiISR(pSW, wpi.INT_EDGE_FALLING, clear)


def loop():
    global globalCounter
    while True:
        rotaryDeal()


# print 'globalCounter = %d' % globalCounter

def destroy():
    print "Program Over"


# GPIO.cleanup()             # Release resource

if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
