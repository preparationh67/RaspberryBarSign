#!/usr/bin/env python
import wiringpi as wpi

pPWM = 26
pwmMinOn = 490
pwmMaxOn = 1024
pwmOn = 0
pwmValue = 800


def setup():
    print "Setup Starting"
    wpi.wiringPiSetup()
    wpi.pinMode(pPWM, wpi.PWM_OUTPUT)
    wpi.pwmWrite(pPWM, 0)


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


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        print "Ended"
