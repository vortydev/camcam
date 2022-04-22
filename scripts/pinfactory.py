########################################################
# Fichier :         pinfactory.py
# Description :     Définition de la classe Pin
# Auteurs :         Étienne Ménard
# Création :        2022/04/22
# Modification :    2022/04/22
########################################################

class Pin:
    __pin = -1

    # init pin
    def __init__(self, p = -1):
        self.pin = p

    # returns the pinNb
    def __repr__(self) -> int:
        return int(self.pin)

    def __str__(self) -> int:
        return int(self.pin)

    # set the pin
    def set_pin(self, p):
        self.pinCheck(p)
        self.__pin = p
        print("Set pin to", p)

    # set the pin
    def get_pin(self):
        return self.__pin

    pin = property(get_pin, set_pin)

    # stops the program if a pin is invalid
    def pinCheck(self, p):
        if (p < 0):
            print("Pin initialisation failed.")
            exit(0)