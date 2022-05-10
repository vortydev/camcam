from client import MQTTClient

mqttClient = MQTTClient("localhost",1883,"Client001","system","sensor","sensor/vibration","sensor/microphone","sensor/gaz","sensor/temperature")

try:
    mqttClient.startMQTT()
except KeyboardInterrupt:
    mqttClient.stopMQTT()