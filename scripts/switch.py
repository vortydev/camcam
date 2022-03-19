########################################################
# Fichier :         switch.py
# Description :     Définition de la classe Switch
# Auteurs :         Étienne Ménard
# Création :        2022/04/22
# Modification :    2022/04/22
########################################################

import RPi.GPIO as GPIO
from scripts.pinfactory import Pin

class Switch:
    pin = Pin(0)

    def __init__(self, pin = 0, mode = GPIO.BCM):
        if (pin > 0):
            self.pin = Pin(pin)
            GPIO.setmode(mode)
            GPIO.setup(self.pin.pinNb, GPIO.IN, GPIO.PUD_UP)
            print ("Initiliased switch with pin {}".format(self.pin.pinNb))
    
