#!/usr/bin/python

import time
import subprocess
import globalVars
from MQTTSend import pubMQTTMsg
import MQTTServer


def wakeonlanRequest(sendFile):
    pubMQTTMsg(MQTTServer.topicWOLPC, MQTTServer.payloadWOLPC)
#    time.sleep(5)  # Esperamos para asegurarnos que el enchufe del PC está realmente encendido

#    command = "/usr/bin/wakeonlan b0:6e:bf:c3:bc:22"
#    subprocess.Popen(command, shell=True)
#    if sendFile:
#        globalVars.toFile(globalVars.sendFile, "Wakeonlan PC")

if __name__ == "__main__":
    wakeonlanRequest(True)
