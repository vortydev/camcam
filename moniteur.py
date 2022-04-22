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
pinGreenLED = 19
pinRedLED = 26
gLED = LED()
rLED = LED()

# switches
pinPwrSwitch = 6
pinFnSwitch = 13
pwrSwitch = Switch()
fnSwitch = Switch()

pinVibration = 18
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
    rLED.turnOn()

    # setup boutons
    global pwrSwitch
    global fnSwitch
    pwrSwitch = Switch(pinPwrSwitch)
    fnSwitch = Switch(pinFnSwitch)

    # init vibration sensor
    global sensorVibration
    sensorVibration = Switch(pinVibration)

    # init microphone
    # init humidity sensor
    # init gas sensor

# main program loop
def loop():
    print("loop!\n")

    if (GPIO.event_detected(pinVibration)):
        print("vibration detected")

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
