import RPi.GPIO as GPIO
from time import sleep

from flask import Flask, request, render_template
from flask_restful import Resource, Api, reqparse, inputs

import threading

import logging
import signal
import sys
import json
import paho.mqtt.client as mqtt

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

app = Flask(__name__)
api = Api(app)
global armer
armer = False

BROKER_HOST = "localhost"
BROKER_PORT = 1883
CLIENT_ID = "AlarmeClient"
TOPICLUMIERE = "lumiere"
TOPICALARME = "alarme"
TOPICPORTE = "porte"
client = None

def thread_function(name):
    main()

def thread_intru(name):
    global armer
    while armer == True:
        GPIO.output(35,GPIO.HIGH)
        GPIO.output(37,GPIO.HIGH)
        GPIO.output(40,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(35,GPIO.LOW)
        GPIO.output(37,GPIO.LOW)
        GPIO.output(40,GPIO.LOW)
        sleep(0.5)


def setup():
    GPIO.setup(35,GPIO.OUT)#principale lumiere
    GPIO.setup(37,GPIO.OUT)#lumiere salon
    GPIO.setup(40,GPIO.OUT)#buzzer

    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#armer
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#porte
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#lumiere

    GPIO.output(35,GPIO.LOW)
    GPIO.output(37,GPIO.LOW)
    GPIO.output(40,GPIO.LOW)

    init_mqtt()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/lumiere')
def allumeLumiere():
    if GPIO.input(35):
        GPIO.output(35,GPIO.LOW)
    else:
        GPIO.output(35,GPIO.HIGH)

@app.route('/armer')
def armerDesarmer():
    global armer
    if armer == False:
        armer = True
        print("Système armé")
    else :
        armer = False
        print("Système désarmé")

@app.route('/porte')
def gestionPorte():
    if armer == False:
        print("La porte à été ouverte")
    else :
        print("La porte à été ouverte, un intru à été détecté")
        threadIntru = threading.Thread(target=thread_intru,args=(1,))
        threadIntru.start()

def on_connect(client, user_data, flags, connection_result_code):                              # (7)
    """on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring."""

    if connection_result_code == 0:                                                            # (8)
        # 0 = successful connection
        logger.info("Connected to MQTT Broker")
    else:
        # connack_string() gives us a user friendly string for a connection code.
        logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))

    client.subscribe(TOPICALARME, qos=2)
    client.subscribe(TOPICLUMIERE, qos=2)
    client.subscribe(TOPICPORTE, qos=2)

def on_disconnect(client, user_data, disconnection_result_code):                               # (10)
    """Called disconnects from MQTT Broker."""
    logger.error("Disconnected from MQTT Broker")

def on_message(client, userdata, msg):                                                         # (11)
    """Callback called when a message is received on a subscribed topic."""
    logger.debug("Received message for topic {}: {}".format( msg.topic, msg.payload))

    data = None

    try:
        data = json.loads(msg.payload.decode("UTF-8"))                                         # (12)
    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: " + msg.payload.decode("UTF-8"))

    if msg.topic == TOPICALARME:                                                                     # (13)
        armerDesarmer()    
    elif msg.topic == TOPICLUMIERE:
        allumeLumiere()
    elif msg.topic == TOPICPORTE:
        gestionPorte()                                                                # (14)

    else:
        logger.error("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))

def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""

    logger.info("You pressed Control + C. Shutting down, please wait...")

    client.disconnect() # Graceful disconnection.
    sys.exit(0)

def init_mqtt():
    global client

    # Our MQTT Client. See PAHO documentation for all configurable options.
    # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
    # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
    # connected.
    client = mqtt.Client(                                                                      # (15)
        client_id=CLIENT_ID,
        clean_session=False)

    # Route Paho logging to Python logging.
    client.enable_logger()                                                                     # (16)

    # Setup callbacks
    client.on_connect = on_connect                                                             # (17)
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)  

def main():
    try:
        global armer
        GPIO.add_event_detect(19,GPIO.RISING)
        GPIO.add_event_detect(21,GPIO.RISING)
        GPIO.add_event_detect(23,GPIO.RISING)
        while True:
            if GPIO.event_detected(23):
                if GPIO.input(35):
                    GPIO.output(35,GPIO.LOW)
                else:
                    GPIO.output(35,GPIO.HIGH)
            if GPIO.event_detected(21):
                print("La porte à été ouverte")
            if GPIO.event_detected(19):
                print("Système armé")
                armer = True
            while armer:
                if GPIO.event_detected(19):
                    print("Système désarmé")
                    armer = False
                    break
                if GPIO.event_detected(23):
                    if GPIO.input(35):
                        GPIO.output(35,GPIO.LOW)
                    else:
                        GPIO.output(35,GPIO.HIGH)
                if GPIO.event_detected(21):
                    print("La porte à été ouverte, un intru à été détecté")
                    while armer == True:
                        GPIO.output(35,GPIO.HIGH)
                        GPIO.output(37,GPIO.HIGH)
                        GPIO.output(40,GPIO.HIGH)
                        sleep(0.5)
                        GPIO.output(35,GPIO.LOW)
                        GPIO.output(37,GPIO.LOW)
                        GPIO.output(40,GPIO.LOW)
                        sleep(0.5)
                        if GPIO.event_detected(19) or armer == False:
                            print("Système désarmé")
                            armer = False
                            break
        
    finally:
        GPIO.cleanup()
    
if __name__ == '__main__':
    setup()
    threadMain = threading.Thread(target=thread_function,args=(1,))
    threadMain.start()

    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C                        # (19)
    logger.info("Listening for messages on topic '" + TOPICALARME + "'. Press Control + C to exit.")

    client.loop_start()                                                                        # (20)
    signal.pause()

    app.run(host="0.0.0.0", debug=False)