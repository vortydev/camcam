########################################################
# Fichier :         client.py
# Description :     Programme du Client Cam-Cam.
# Auteurs :         Étienne Ménard, Isabelle Rioux
# Création :        2022/04/13
# Modification :    2022/04/13
########################################################

from camcam.scripts.alarmemosquitto import init_mqtt
import paho.mqtt.client as mqtt

class MQTTClient:
    __brokerHost = "localhost"
    __brokerPort = 1883
    __idClient = "Client001"
    __client = None

    def __init__(self, brokerHost, brokerPort, idClient):
        self.__brokerHost = brokerHost
        self.__brokerPort = brokerPort
        self.__idClient = idClient

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

    def init_mqtt(self):
        global client
        client = mqtt.Client(
            client_id = self.idClient,
            clean_session = False
        )

        # Route Paho logging to Python logging.
        # client.enable_logger()

        # Setup callbacks
        # client.on_connect = on_connect
        # client.on_disconnect = on_disconnect
        # client.on_message = on_message

        # Connect to Broker.
        client.connect(self.brokerHost, self.brokerHost)
