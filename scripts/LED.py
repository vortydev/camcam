########################################################
# Fichier :         LED.py
# Description :     Définition de la classe LED
# Auteurs :         Étienne Ménard
# Création :        2022/04/22
# Modification :    2022/04/22
########################################################

import RPi.GPIO as GPIO
from scripts.pinfactory import Pin

class LED:
    pin = Pin(0)

    def __init__(self, pin = 0, mode = GPIO.BCM):
        if (pin > 0):
            self.pin = Pin(pin)
            GPIO.setmode(mode)
            GPIO.setup(self.pin.pinNb, GPIO.OUT)
            print ("Initiliased LED with pin {}".format(pin))

    def turnOn(self, debug = False):
        GPIO.output(self.pin.pinNb, GPIO.HIGH)
        if (debug):
            print("LED on!")

    def turnOff(self, debug = False):
        GPIO.output(self.pin.pinNb, GPIO.LOW)
        if (debug):
            print("LED off!")
