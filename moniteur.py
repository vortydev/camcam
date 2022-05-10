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
import math

import RPi.GPIO as GPIO

import threading

from scripts.ADCDevice import *
from scripts.LED import LED
from scripts.switch import Switch
from client import MQTTClient
#ask for broker ip address?
#should have launched the broker on client side
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

mqttClient = MQTTClient("localhost",1883,"Moniteur001","system","sensor","sensor/vibration","sensor/microphone","sensor/gaz","sensor/temperature")

threadLoop = None
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
    print("\n!\tSYSTEM INITIALISATION\t!")

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

    mqttClient.client.loop_start()

def datetime2float(date):
    epoch = datetime.utcfromtimestamp(0)
    seconds =  (date - epoch).total_seconds()
    return seconds

def float2datetime(fl):
    return datetime.fromtimestamp(fl)

def powerButton():
    global timestamp
    trigger = timestamp + timedelta(seconds=3)
    now = datetime.now()

    if (now > trigger):
        if (ONLINE):
            systemOffline()
        else:
            systemOnline()

        timestamp = datetime.now()

def resetButton():
    global timestamp
    trigger = timestamp + timedelta(seconds=5)
    now = datetime.now()
    flNow = datetime2float(now)
    
    if (now > timestamp + timedelta(seconds=2)):
        if (flNow <= math.floor(flNow)+0.5):
            gLED.turnOn()
        else:
            gLED.turnOff()

    if (now > trigger):
        if (ONLINE):
            for i in range(0, 5):
                gLED.turnOn()
                sleep(0.1)
                gLED.turnOff()
                sleep(0.1)
            systemReset()
            timestamp = datetime.now()

def systemOnline():
    print("\n!\tSYSTEM ONLINE\t!")
    global ONLINE
    ONLINE = True
    rLED.turnOn()

def systemOffline():
    print("\n!\tSYSTEM OFFLINE\t!")
    global ONLINE
    ONLINE = False
    rLED.turnOff()

def systemReset():
    print("\n!\tSYSTEM RESET\t!")

    # init adc
    global adc
    if (adc.detectI2C(0x4b)):
        adc = ADS7830()
    elif (adc.detectI2C(0x48)):
        adc = PCF8591()
    else:
        print("No correct I2C address found.")
        exit(-1)
    
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

    # init vibration sensor
    global sensorVibration
    sensorVibration = Switch(pinVibration)

    # init humidity sensor
    global dht
    dht = DHT.DHT(pinDHT)

    # time
    global timestamp
    timestamp = datetime.now()

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
    return gasVal
    # print("analog value: %03d  Gas concentration: %d\n"%(gasVal, concentration))

# read microphone value from adc
def routineMic():
    micVal = adc.analogRead(1)
    volume = 255 - micVal
    return volume
    # print("analog value: %03d  volume: %d\n"%(micVal, volume))

# read values from DHT
def routineDHT():
    chk = dht.readDHT11()     #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
    # if (chk == dht.DHTLIB_OK):      #read DHT11 and get a return value. Then determine whether data read is normal according to the return value.
        # print("DHT11,OK!")

    # dht.humidity
    # dht.temperature
    return ({'humidity':dht.humidity, 'temperature':dht.temperature})

    # print("Humidity : %.2f\nTemperature : %.2f \n"%(dht.humidity,dht.temperature))

# main program loop
def loop():
    global timestamp
    while (True):
        # update timestamp on btn click
        if (GPIO.event_detected(pinPwrSwitch)):    
            timestamp = datetime.now()
        elif (GPIO.event_detected(pinFnSwitch)):
            timestamp = datetime.now()

        # power on and off
        if (GPIO.input(pinPwrSwitch) == 0):
            powerButton()

        if (GPIO.input(pinFnSwitch) == 0 and GPIO.input(pinPwrSwitch) == 1):
            resetButton()

        if (ONLINE):
            # vibration
            if (GPIO.event_detected(pinVibration)):
                print("vibration detected")
                vibeJSON = {'vibe':'yes'}
                mqttClient.publish(mqttClient.topicVibration,vibeJSON)
            
            # gas
            mqttClient.publish(mqttClient.topicGaz, {'gaz':routineGas()})

            # microphone
            mqttClient.publish(mqttClient.topicMicrophone, {'mic':routineMic()})
            
            # DHT
            mqttClient.publish(mqttClient.topicTemperature, routineDHT())
        sleep(0.1)

def thread_loop(name):
    loop()

# cleanup sequence
def destroy():
    print("\n!\tSYSTEM CLEANUP\t!")
    mqttClient.client.loop_stop()
    adc.close()
    GPIO.cleanup()

# main
if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt: # Capture Ctrl-c, appelle destroy, puis quitte
        destroy()
