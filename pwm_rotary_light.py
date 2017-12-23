#!/usr/bin/env python
import wiringpi as wpi
import datetime

# Pins
pCLK = 3  # BCM 22
pDT = 4  # BCM 23
pSW = 5  # BCM 24
pSideLight = 25
pPWM = 26  # BCM 12
inputPins = [pCLK, pDT, pSW]

# Rotary Knob Vars
flag = 0
Last_DT_Status = 0
Current_DT_Status = 0
LastClearTime = 0

# PWM Vars
pwmMinOn = 490
pwmLow = 520
pwmHigh = 890
pwmStrobe = 1000
pwmMaxOn = 1024
pwmValue = 800

# Side Lights
sideLightsOn = wpi.LOW

# Light States
lightStates = ['Off', 'MainOffSideOn', 'MainLowSideOff', 'MainLowSideOn',
               'MainHighSideOff', 'MainHighSideOn', 'SoftOff']
# 0, 1, 2, 3, 4, 5, 6
currentState = 0
lastState = 0


def setup():
    global pwmValue
    print "Setup Starting"
    wpi.wiringPiSetup()
    for pin in inputPins:
        wpi.pinMode(pin, wpi.INPUT)
    wpi.pullUpDnControl(pSW, wpi.PUD_UP)
    wpi.pinMode(pSideLight, wpi.OUTPUT)
    wpi.digitalWrite(pSideLight, sideLightsOn)
    wpi.pinMode(pPWM, wpi.PWM_OUTPUT)
    pwmValue = 0
    wpi.pwmWrite(pPWM, pwmValue)
    rotaryButtonSetup()


def destroy():
    print "Program Over"


def loop():
    print "Starting Program Loop"
    while True:
        rotaryScan()


def updateOnState():
    global pwmValue
    global sideLightsOn
    print "Updating State"
    if currentState == 0:
        pwmValue = 0
        sideLightsOn = wpi.LOW
    elif currentState == 1:
        pwmValue = 0
        sideLightsOn = wpi.HIGH
    elif currentState == 2:
        pwmValue = pwmLow
        sideLightsOn = wpi.LOW
    elif currentState == 3:
        pwmValue = pwmLow
        sideLightsOn = wpi.HIGH
    elif currentState == 4:
        pwmValue = pwmHigh
        sideLightsOn = wpi.LOW
    elif currentState == 5:
        pwmValue = pwmHigh
        sideLightsOn = wpi.HIGH
    wpi.digitalWrite(pSideLight, sideLightsOn)
    wpi.pwmWrite(pPWM, pwmValue)


def rotaryScan():
    global flag
    global Last_DT_Status
    global Current_DT_Status
    global currentState
    Last_DT_Status = wpi.digitalRead(pDT)
    while not wpi.digitalRead(pCLK):
        Current_DT_Status = wpi.digitalRead(pDT)
        flag = 1
    if flag == 1:
        flag = 0
        if (Last_DT_Status == 0) and (Current_DT_Status == 1):
            currentState = currentState + 1 if currentState + 1 < 6 else 0  # Increment State
            print 'currentState = %d' % currentState
        if (Last_DT_Status == 1) and (Current_DT_Status == 0):
            currentState = currentState - 1 if currentState - 1 > -1 else 5  # Decrement State
            print 'currentState = %d' % currentState
        updateOnState()


def softOff():
    global LastClearTime
    global currentState
    global lastState
    if LastClearTime == 0 or (datetime.datetime.now() - LastClearTime) > datetime.timedelta(seconds=1):
        if currentState != 0:
            wpi.pwmWrite(pPWM, 0)
            wpi.digitalWrite(pSideLight, 0)
            lastState = currentState
            currentState = 6
            print "Soft Off Activated"
        elif currentState == 6:
            wpi.pwmWrite(pPWM, pwmValue)
            wpi.digitalWrite(pSideLight, sideLightsOn)
            currentState = lastState
            lastState = 6
            print "Returning from soft off"
        LastClearTime = datetime.datetime.now()


def rotaryButtonSetup():
    wpi.wiringPiISR(pSW, wpi.INT_EDGE_FALLING, softOff)  # wait for falling


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
