########################################################
# Fichier :         LED.py
# Description :     Classe pour générer des objets LED.
# Auteurs :         Étienne Ménard
# Création :        2022/04/22
# Modification :    2022/04/22
########################################################

import RPi.GPIO as GPIO

class LED:
    __pin = -1

    def __init__(self, pinNb = -1):
        if (pinNb != -1):
            self.pin = pinNb
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pinNb, GPIO.OUT)

    def set_pin(self, pinNb):
        self.__pin = pinNb
        print("LED set to pin", pinNb)

    def get_pin(self):
        return self.__pin

    pin = property(get_pin, set_pin)

    def turnOn(self):
        GPIO.output(self.pin, GPIO.HIGH)
        print("LED on!")

    def turnOff(self):
        GPIO.output(self.pin, GPIO.LOW)
        print("LED off!")
