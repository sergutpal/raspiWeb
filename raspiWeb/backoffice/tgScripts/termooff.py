# -*- coding: utf-8 -*-
from MQTTSend import pubMQTTMsg
import MQTTServer
import globalVars

if __name__ == "__main__":
    pubMQTTMsg(MQTTServer.topicTermo, MQTTServer.payloadAlarmaOFF)
    globalVars.toFile(globalVars.sendFile, "Termo apagado por telegram")

