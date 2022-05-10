# Cam Cam
Projet de fin de session du programme de Techniques de l'informatique du Cégep de Sherbrooke.

&nbsp;

## Tableau de connections électriques

### Tableau de connexions pour le *header* du *Raspberry Pi*.

| # *pin* | Nom E/S | Connecté à |
|-|-|-|
| 2 | SDA 1 | ADC |
| 3 | SCL 1 | ADC |
| 5 | GPIO 5 | DEL verte |
| 6 | GPIO 6 | DEL rouge |
| 13 | GPIO 13 | Bouton jaune (*reset switch*) |
| 19 | GPIO 19 | Bouton rouge (*power switch*) |
| 25 | GPIO 25 | DHT |
| 27 | GPIO 27 | Vibration Sensor Module (*switch*) |

### Tableau de connexions pour l'ADC ADS7830.
| # *pin* | Nom E/S | Connecté à |
|-|-|-|
| 1 | CH0 | MQ-2 Gas Sensor Module |
| 2 | CH1 | MIC Module |
| 14 | SCL | Raspberry Pi |
| 15 | SDA | Raspberry Pi |

&nbsp;

## Fichiers
- [client.py](client.py)
- [moniteur.py](moniteur.py)
- [LED.py](./scripts/LED.py)
- [pinfactory.py](./scripts/pinfactory.py)
- [switch.py](./scripts/switch.py)

&nbsp;

## Documentation

- [MQ-2 Gas Sensor](https://www.manualslib.com/manual/1813326/Adeept-Ultimate-Sensor-Kit-For-Raspberry-Pi.html?page=121#manual)
- [Sound Sensor](https://www.manualslib.com/manual/1813326/Adeept-Ultimate-Sensor-Kit-For-Raspberry-Pi.html?page=125#manual)
- [Vibration Switch](https://www.manualslib.com/manual/1813326/Adeept-Ultimate-Sensor-Kit-For-Raspberry-Pi.html?page=55#manual)
- [Adeept Python Repo](https://github.com/adeept/Adeept_Sensor_Kit_for_RPi_Python_Code)
- [MQTT stuff](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [More MQTT stuff](http://www.steves-internet-guide.com/into-mqtt-python-client/)
- [Remote MQTT stuff](http://www.steves-internet-guide.com/mosquitto-bridge-configuration/)
- [Maybe this for 2 pi together](https://mohamedelhlafi.medium.com/use-the-mqtt-protocol-to-communicate-data-between-2-raspberry-pi-3d432dea9313)

&nbsp;

## Auteurs
- Étienne Ménard
- Isabelle Rioux
