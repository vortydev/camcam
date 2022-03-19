########################################################
# Fichier :         moniteur.py
# Description :     Programme du Moniteur Cam-Cam.
# Auteurs :         Étienne Ménard, Isabelle Rioux
# Création :        2022/04/13
# Modification :    2022/04/20
########################################################

########################
#     IMPORTATIONS     #
########################

from time import sleep

import RPi.GPIO as GPIO

from scripts.LED import LED
from scripts.switch import Switch

#####################
#     VARIABLES     #
#####################

# LEDs
pinGreenLED = 5
pinRedLED = 6
gLED = LED()
rLED = LED()

# switches
pinPwrSwitch = 19
pinFnSwitch = 13
pwrSwitch = Switch()
fnSwitch = Switch()

pinVibration = 27
sensorVibration = Switch()


#####################
#     FONCTIONS     #
#####################

# initialisation
def setup():
    print("setting up...\n")
    GPIO.setmode(GPIO.BCM)
    
    # setup LEDs
    global gLED
    global rLED
    gLED = LED(pinGreenLED)
    rLED = LED(pinRedLED)
    gLED.turnOff()
    rLED.turnOff()

    # setup boutons
    global pwrSwitch
    global fnSwitch
    pwrSwitch = Switch(pinPwrSwitch)
    fnSwitch = Switch(pinFnSwitch)
    GPIO.add_event_detect(pinPwrSwitch, GPIO.FALLING)
    GPIO.add_event_detect(pinFnSwitch, GPIO.FALLING)

    # init vibration sensor
    global sensorVibration
    sensorVibration = Switch(pinVibration)
    GPIO.add_event_detect(sensorVibration.pin.pinNb, GPIO.FALLING)

    # init microphone
    # init humidity sensor
    # init gas sensor

# def callback_pwrSwitch(channel):
#     print("pwr button clicked")

# def callback_fnSwitch(channel):
#     print("fn button clicked")

# def callback_vibration(channel):
#     print("vibration switch triggered")

# main program loop
def loop():
    while (True):
        if (GPIO.event_detected(pinVibration)):
            print("vibration detected")

        if (GPIO.event_detected(pinPwrSwitch)):
            print("pwr switch detected")

        if (GPIO.event_detected(pinFnSwitch)):
            print("fn switch detected")

        sleep(0.1)

# cleanup sequence
def destroy():
    print("destroying!\n")
    GPIO.cleanup()

# main
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()
