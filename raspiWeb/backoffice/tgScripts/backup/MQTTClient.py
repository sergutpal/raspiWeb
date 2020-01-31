#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import json
from globalVars import toLogFile
from alarma import setAlarmOn
from alarmaoff import setAlarmOff
from auto import setAlarmAutoOn
from autooff import setAlarmAutoOff
import globalVars

mqttc = None
topicParkingOpen = "parking/open"
payloadParkingOpen = b'{"open":"true"}'
topicZigbee2mqtt = "zigbee2mqtt"


def on_message(mqttc, obj, msg):
    try:
#       toLogFile("On message recibido")
       s = "MQTT - Topic: @" + msg.topic + "@. Payload: @" + str(msg.payload) + "@"
       toLogFile(s)
       if (msg.topic == topicParkingOpen) and (msg.payload ==payloadParkingOpen):
           globalVars.toFile(globalVars.sendFile, "Atención: petición MQTT abrir parking!!")
       if msg.topic == globalVars.topicAlarma:
           if (msg.payload ==globalVars.payloadAlarmaON):
               setAlarmOn('MQTT')
           if (msg.payload ==globalVars.payloadAlarmaOFF):
               setAlarmOff()
       if msg.topic == globalVars.topicAlarmaAuto:
           toLogFile("Topic AlarmaAuto")
           if (msg.payload ==globalVars.payloadAlarmaON):
               setAlarmAutoOn('MQTT')
           if (msg.payload ==globalVars.payloadAlarmaOFF):
               setAlarmAutoOff('MQTT')
       #if msg.topic == topicZigbee2mqtt:

    except Exception as e:
        toLogFile('Error on_message: ' + str(e))


def iniMQTT():
    global mqttc

    if (globalVars.raspiId =="0") and (mqttc is None):
        try:
            mqttc = mqtt.Client()
            mqttc.on_message = on_message
            mqttc.username_pw_set(username=globalVars.mqttUser,password=globalVars.mqttPwd)
            mqttc.connect(globalVars.mqttSrv, globalVars.mqttPort, 60)
            mqttc.subscribe(topicParkingOpen, 0)
            mqttc.subscribe(topicAlarma, 0)
            mqttc.subscribe(topicAlarmaAuto, 0)
            mqttc.loop_start()
            return True
        except Exception as e:
            toLogFile('Error initMQTT: ' + str(e))
            return False


def openParkingMQTT():
    global mqttc
    global topicParkingOpen

    if globalVars.raspiId !="0":
        return False
    try:
        return pubMQTTMsg(topicParkingOpen, "open")
    except Exception as e:
        toLogFile('Error openParking: ' + str(e))
        return False


def loopMQTT():
    global mqttc

    iniMQTT()
    try:
        if mqttc is not None:
            mqttc.loop()
        return True
    except Exception as e:
        toLogFile('Error loopMQTT: ' + str(e))
        mqttc = None
        return False


def pubMQTTMsg(topic, payload):
    global mqttc

    iniMQTT()
    try:
        if mqttc is not None:
            mqttc.publish(topic, payload)
        return True
    except Exception as e:
        toLogFile('Error pubMQTTMsg: ' + str(e))
        mqttc = None
        return False





#if __name__ == "__main__":
#    iniMQTT()
