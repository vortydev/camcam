#!/usr/bin/env python3

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
from datetime import datetime
from datetime import timedelta

import RPi.GPIO as GPIO

from scripts.ADCDevice import *
from scripts.LED import LED
from scripts.switch import Switch
import scripts.Freenove_DHT as DHT

#####################
#     VARIABLES     #
#####################

# adc object
adc = ADCDevice()

# LEDs
pinGreenLED = 5
pinRedLED = 6
gLED = LED()    # data LED
rLED = LED()    # pwr LED

# switches
pinPwrSwitch = 19
pinFnSwitch = 13
pwrSwitch = Switch()
fnSwitch = Switch()

# vibration sensor
pinVibration = 27
sensorVibration = Switch()

# dht object
pinDHT = 25
dht = DHT.DHT(0)

# MONITEUR
ONLINE = False
timestamp = 0

#####################
#     FONCTIONS     #
#####################

# initialisation
def setup():
    print("setting up...\n")

    # init adc
    global adc
    if (adc.detectI2C(0x4b)):
        adc = ADS7830()
    elif (adc.detectI2C(0x48)):
        adc = PCF8591()
    else:
        print("No correct I2C address found.")
        exit(-1)

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

    # init humidity sensor
    global dht
    dht = DHT.DHT(pinDHT)

    # time
    global timestamp
    timestamp = datetime.now()

def powerButton():
    global timestamp
    trigger = timestamp + timedelta(seconds=3)
    now = datetime.now()
    if (trigger < now):
        if (ONLINE):
            systemOffline()
        else:
            systemOnline()
        
        timestamp = datetime.now()

def systemOnline():
    print("\n!\tSYSTEM: ONLINE")
    global ONLINE
    ONLINE = True
    rLED.turnOn()

def systemOffline():
    print("\n!\tSYSTEM: OFFLINE")
    global ONLINE
    ONLINE = False
    rLED.turnOff()

# def callback_pwrSwitch(channel):
    # print("pwr button clicked")    

# def callback_fnSwitch(channel):
    # print("fn button clicked")

# def callback_vibration(channel):
    # print("vibration switch triggered")

# read gas sensor value from adc
def routineGas():
    gasVal = adc.analogRead(0)
    concentration = gasVal
    # print("analog value: %03d  Gas concentration: %d\n"%(gasVal, concentration))

# read microphone value from adc
def routineMic():
    micVal = adc.analogRead(1)
    volume = 255 - micVal
    # print("analog value: %03d  volume: %d\n"%(micVal, volume))

# read values from DHT
def routineDHT():
    chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    # if (chk is dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        # print("DHT11,OK!")

    # print("Humidity : %.2f\nTemperature : %.2f \n"%(dht.humidity,dht.temperature))

# main program loop
def loop():
    while (True):
        # update timestamp on btn click
        if (GPIO.event_detected(pinPwrSwitch)):
                global timestamp
                timestamp = datetime.now()

        # power on and off
        if (GPIO.input(pinPwrSwitch) == 0):
            powerButton()

        if (ONLINE):
            
                # print(timestamp)

            

            # elif (GPIO.input(pinPwrSwitch) == 1):
            #     global timer
            #     timer = 0

            

            # if (GPIO.event_detected(pinFnSwitch)):
            #     print("fn switch detected")

            # vibration
            if (GPIO.event_detected(pinVibration)):
                print("vibration detected")
            
            # gas
            routineGas()

            # microphone
            routineMic()
            
            # DHT
            routineDHT()

        sleep(0.1)

# cleanup sequence
def destroy():
    print("destroying!\n")
    adc.close()
    GPIO.cleanup()

# main
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()
