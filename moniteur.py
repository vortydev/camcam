########################################################
# Fichier :         moniteur.py
# Description :     Programme du Moniteur Cam-Cam.
# Auteurs :         Étienne Ménard, Isabelle Rioux
# Création :        2022/04/13
# Modification :    2022/04/13
########################################################

########################
#     IMPORTATIONS     #
########################

# import RPi.GPIO as GPIO



#####################
#     FONCTIONS     #
#####################

# initialisation
def setup():
    print("setting up...\n")
    # GPIO.setmode(GPIO.BCM)  

# main program loop
def loop():
    print("loop!\n")

# cleanup sequence
def destroy():
    print("destroying!\n")
    # GPIO.cleanup()

# main
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()
