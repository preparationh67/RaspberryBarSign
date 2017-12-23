#!/usr/bin/env python
import wiringpi as wpi
import datetime

# Pins
pCLK = 3  # BCM 22
pDT = 4  # BCM 23
pSW = 5  # BCM 24
pPWM = 26  # BCM 12
inputPins = [pCLK, pDT, pSW]

# Rotary Knob Vars
globalCounter = 24
flag = 0
Last_DT_Status = 0
Current_DT_Status = 0
LastClearTime = 0

# PWM Vars
pwmMinOn = 490
pwmMaxOn = 1024
pwmOn = 0
pwmValue = 800


def setup(light_off=False):
    global pwmOn
    global pwmValue
    print "Setup Starting"
    wpi.wiringPiSetup()
    for pin in inputPins:
        wpi.pinMode(pin, wpi.INPUT)
    wpi.pullUpDnControl(pSW, wpi.PUD_UP)
    wpi.pinMode(pPWM, wpi.PWM_OUTPUT)
    pwmOn = True
    if light_off:
        pwmValue = 0
        pwmOn = False
    wpi.pwmWrite(pPWM, pwmValue)


def destroy():
    print "Program Over"


def loop():
    global pwmValue
    while True:
        pwmIn = input("0,490-1024: ")
        pwmValue = int(pwmIn)
        if pwmValue < pwmMinOn:
            pwmValue = 0
        if pwmValue > pwmMaxOn:
            pwmValue = pwmMaxOn
        wpi.pwmWrite(pPWM, pwmValue)


def rotaryScan():
    global flag
    global Last_DT_Status
    global Current_DT_Status
    global globalCounter
    Last_DT_Status = wpi.digitalRead(pDT)
    while not wpi.digitalRead(pCLK):
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


def clear():
    global LastClearTime
    global globalCounter
    if LastClearTime == 0 or (datetime.datetime.now() - LastClearTime) > datetime.timedelta(seconds=1):
        globalCounter = 0
        print 'globalCounter = %d' % globalCounter
        LastClearTime = datetime.datetime.now()


def rotaryClear():
    wpi.wiringPiISR(pSW, wpi.INT_EDGE_FALLING, clear)  # wait for falling


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
