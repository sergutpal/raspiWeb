#!/usr/bin/python
# -*- coding: utf-8 -*-


mqttSrv = "192.168.1.20"
mqttPort = 1883
mqttUser = "sergutpal"
mqttPwd = "SGp24121976"

topicAlarma = "raspi/alarma"
topicAlarmaAuto = "raspi/alarmaAuto"
topicRadioParking = "raspi/radioParking"
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
topicHumo = "zigbee2mqtt/HumoX"

topicWOLPC = "zigbee2mqtt/SonoffPC/set"
payloadWOLPC = b'{"state":"ON","linkquality":0}'
payloadPCOFF = b'{"state":"OFF","linkquality":0}'

topicGetTemperaturas = "getTemperatures"

topicRTL433 = "RTL433/cmd"
payloadRTL433Timbre1 = "899219"  # Timbre real
payloadRTL433Timbre2 = "25742"   # Timbre real
payloadRTL433Parking1 = "651568" # Parking real
payloadRTL433Parking2 = "1607"   # Parking real
payloadRTL433Parking3 = "4656"   # Parking real
payloadRTL433Parking4 = "827952" # Parking real
payloadRTL433Naranja = "602592"  # WOL

topicClick1 = "zigbee2mqtt/Click1/action"
payloadClickSingle = b'single'
payloadClickDouble = b'double'
payloadClickHold = b'hold'

