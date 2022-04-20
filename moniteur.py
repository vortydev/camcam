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
from scripts.vibration import Vibration



#####################
#     VARIABLES     #
#####################

pinGreenLED = 19
pinRedLED = 26
# TODO LED object

pinPwrSwitch = 6
pinFnSwitch = 13
# TODO switch object

pinVibration = 18   # temp
sensorVibration = Vibration()


#####################
#     FONCTIONS     #
#####################

# initialisation
def setup():
    print("setting up...\n")
    GPIO.setmode(GPIO.BCM)
    
    # setup LEDs
    # setup boutons

    # init vibration sensor
    global sensorVibration
    sensorVibration = Vibration(pinVibration)

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
