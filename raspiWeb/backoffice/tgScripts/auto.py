#!/usr/bin/python

import globalVars
import os
import sys
import MQTTServer
from MQTTSend import pubMQTTMsg


def setAlarmAutoOn(cron=False):
    if (cron):
        # Si el parametro es cron, quiere decir que la peticion viene de la tarea del cron y
        # hay que comprobar si el modo auto del cron esta activo en la BD config.
       if globalVars.getConfigField('alarmCronAutoActive') =='0':
          return True

    if (globalVars.setAlarmAuto(True)):
        globalVars.toFile(globalVars.sendFile, 'Alarma en modo Automatico ON')
    else:
        globalVars.toFile(globalVars.sendFile,
                          "No se ha podido actualizar el estado de la alarma!")


if __name__ == "__main__":
    pubMQTTMsg(MQTTServer.topicAlarmaAuto, MQTTServer.payloadAlarmaON)
