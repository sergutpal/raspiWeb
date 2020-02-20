#!/usr/bin/python
# -*- coding: utf-8 -*-


mqttSrv = "192.168.1.20"
mqttPort = 1883
mqttUser = "sergutpal"
mqttPwd = "SGp24121976"

topicAlarma = "raspi/alarma"
topicAlarmaAuto = "raspi/alarmaAuto"
payloadAlarmaON = b'ON'
payloadAlarmaOFF = b'OFF'

topicParkingOpen = "esp8266PKG/cmd"
payloadParkingOpen = 'parking'
topicPuertaParking = "zigbee2mqtt/Door1"



topicTimbre = "raspi/timbre"
payloadTimbre = b'ON'

topicEfergy = "efergy"

topicAqaraMotion = "zigbee2mqtt/MoveX"
topicAqaraDoor = "zigbee2mqtt/DoorX"
topicHumoSalon = "zigbee2mqtt/HumoSalon"

topicWOLPC = "zigbee2mqtt/SonoffPC/set"
payloadWOLPC = b'{"state":"ON","linkquality":0}'
payloadPCOFF = b'{"state":"OFF","linkquality":0}'

topicGetTemperaturas = "getTemperatures"
