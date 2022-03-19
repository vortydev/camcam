########################################################
# Fichier :         client.py
# Description :     Programme du Client Cam-Cam.
# Auteurs :         Étienne Ménard, Isabelle Rioux
# Création :        2022/04/13
# Modification :    2022/04/20
########################################################

#from camcam.scripts.alarmemosquitto import init_mqtt
import json
import sys
import signal
import paho.mqtt.client as mqtt

class MQTTClient:
    __brokerHost = "localhost"  # curl ifconfig.me to get public ip address
    __brokerPort = 1883
    __idClient = "Client001"
    __client = None
    __topicSystem = "system"
    __topicSensor = "sensor"
    __topicVibration = "sensor/vibration"
    __topicMicrophone = "sensor/microphone"
    __topicGaz = "sensor/gaz"
    __topicTemperature = "sensor/temperature"

    def __init__(self, brokerHost, brokerPort, idClient, topicSystem, topicSensor, topicVibration, topicMicrophone, topicGaz, topicTemperature):
        self.__brokerHost = brokerHost
        self.__brokerPort = brokerPort
        self.__idClient = idClient
        self.__topicSystem = topicSystem
        self.__topicSensor = topicSensor
        self.__topicVibration = topicVibration
        self.__topicMicrophone = topicMicrophone
        self.__topicGaz = topicGaz
        self.__topicTemperature = topicTemperature

        init_mqtt(self)

    # brokerHost
    def set_brokerHost(self, host):
        self.__brokerHost = host

    def get_brokerHost(self):
        return self.__brokerHost

    brokerHost = property(get_brokerHost, set_brokerHost)

    # brokerPort
    def set_brokerPort(self, port):
        self.__brokerPort = port

    def get_brokerPort(self):
        return self.__brokerPort

    brokerPort = property(get_brokerPort, set_brokerPort)

    # idClient
    def set_idClient(self, id):
        self.__idClient = id

    def get_idClient(self):
        return self.__idClient

    idClient = property(get_idClient, set_idClient)

    # topicSystem
    def set_topicSystem(self, topicSystem):
        self.__topicSystem = topicSystem

    def get_topicSystem(self):
        return self.__topicSystem

    topicSystem = property(get_topicSystem, set_topicSystem)

    # topicSensor
    def set_topicSensor(self, topicSensor):
        self.__topicSensor = topicSensor

    def get_topicSensor(self):
        return self.__topicSensor

    topicSensor = property(get_topicSensor, set_topicSensor)

    # topicVibration
    def set_topicVibration(self, topicVibration):
        self.__topicVibration = topicVibration

    def get_topicVibration(self):
        return self.__topicVibration

    topicVibration = property(get_topicVibration, set_topicVibration)

    # topicMicrophone
    def set_topicMicrophone(self, topicMicrophone):
        self.__topicMicrophone = topicMicrophone

    def get_topicMicrophone(self):
        return self.__topicMicrophone

    topicMicrophone = property(get_topicMicrophone, set_topicMicrophone)

    # topicGaz
    def set_topicGaz(self, topicGaz):
        self.__topicGaz = topicGaz

    def get_topicGaz(self):
        return self.__topicGaz

    topicGaz = property(get_topicGaz, set_topicGaz)

    # topicTemperature
    def set_topicTemperature(self, topicTemperature):
        self.__topicTemperature = topicTemperature

    def get_topicTemperature(self):
        return self.__topicTemperature
    
    topicTemperature = property(get_topicTemperature, set_topicTemperature)

    def on_connect(client, user_data, flags, connection_result_code):
        if connection_result_code == 0:
            print("Connected to MQTT Broker")
        else:
            print("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))

        client.subscribe(self.topicSystem, qos=2)
        client.subscribe(self.topicSensor, qos=2)
        client.subscribe(self.topicVibration, qos=2)
        client.subscribe(self.topicMicrophone, qos=2)
        client.subscribe(self.topicGaz, qos=2)
        client.subscribe(self.topicTemperature, qos=2)

    def on_disconnect(client, user_data, disconnection_result_code):
        print("Disconnected from MQTT broker")

    def on_message(self, client, user_data, msg):
        print("Received message for topic {}: {}".format( msg.topic, msg.payload))
        data = None
        try:
            data = json.loads(msg.payload.decode("UTF-8"))
        except json.JSONDecodeError as e:
            print("JSON Decode Error: " + msg.payload.decode("UTF-8"))

        if msg.topic == self.topicSystem:
            print("Etat du systeme")
        elif msg.topic == self.topicSensor:
            print("Tout les sensor")
        elif msg.topic == self.topicVibration:
            print("Vibration")
        elif msg.topic == self.topicMicrophone:
            print("Microphone")
        elif msg.topic == self.topicGaz:
            print("Gaz")
        elif msg.topic == self.topicTemperature:
            print("Temperature")
        else:
            print("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))

    def signal_handler(sig, frame):
        print("You pressed Control + C. Shutting down, please wait...")

        client.disconnect()
        sys.exit(0)

    def init_mqtt(self):
        global client
        client = mqtt.Client(
            client_id = self.idClient,
            clean_session = False
        )

        # Route Paho logging to Python logging.
        # client.enable_logger()

        # Setup callbacks
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message

        # Connect to Broker.
        client.connect(self.brokerHost, self.brokerHost)

    def startMQTT(self):
        signal.signal(signal.SIGINT, signal_handler)
        print("Listening for messages on topic '" + TOPIC + "'. Press Control + C to exit.")
        client.loop_start()
        signal.pause()
