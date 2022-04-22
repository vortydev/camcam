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
            GPIO.setup(self.pin.pin, GPIO.OUT)
            print ("initiliased LED with pin {}".format(self.pin))

    def turnOn(self):
        GPIO.output(self.pin.pin, GPIO.HIGH)
        print("LED on!")

    def turnOff(self):
        GPIO.output(self.pin.pin, GPIO.LOW)
        print("LED off!")
