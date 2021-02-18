# -*- coding: utf-8 -*-
from MQTTSend import pubMQTTMsg
import MQTTServer
import globalVars


if __name__ == "__main__":
    pubMQTTMsg(MQTTServer.topicCaldera, MQTTServer.payloadAlarmaON)
    globalVars.toFile(globalVars.sendFile, "Caldera encendida por telegram")

