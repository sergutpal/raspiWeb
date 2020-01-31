#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import json
from globalVars import toLogFile
import globalVars
import MQTTServer
import time

def iniMQTT(clientId):
    try:
        mqttc = mqtt.Client(client_id=clientId)
        mqttc.username_pw_set(username=MQTTServer.mqttUser,password=MQTTServer.mqttPwd)
        mqttc.connect(MQTTServer.mqttSrv, MQTTServer.mqttPort)
        return mqttc
    except Exception as e:
        toLogFile('Error initMQTT: ' + str(e))
        return None

def pubMQTTMsg(topic, payload, qos=0, clientId="", retain=False):
    global mqttc

    mqttc = iniMQTT(clientId)
    try:
        if mqttc is not None:
            #toLogFile('publicando MQTT: ' + str(topic) + ' - ' + str(payload))
            mqttc.publish(topic, payload, qos, retain)
            mqttc.disconnect()
        return True
    except Exception as e:
        toLogFile('Error pubMQTTMsg: ' + str(e))
        # mqttc.disconnect()
        return False