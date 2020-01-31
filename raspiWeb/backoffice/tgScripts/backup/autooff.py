#!/usr/bin/python

import globalVars
import os
import sys

def setAlarmAutoOff(cron):
    if (cron):
        # Si el parametro es cron, quiere decir que la peticion viene de la tarea del cron y
        # hay que comprobar si el modo auto del cron esta activo en la BD config.
       if globalVars.getConfigField('alarmCronAutoActive') =='0':
          return True

    if (globalVars.setAlarmAuto(False)):
        globalVars.toFile(globalVars.sendFile, 'Modo automático alarma OFF')
    else:
        globalVars.toFile(globalVars.sendFile,
                          "No se ha podido actualizar el estado auto de la alarma!")


if __name__ == "__main__":
    try:
        cron = len(sys.argv) >=2 and sys.argv[1].lower() =='cron'
    except Exception as e:
        cron = False

    setAlarmAutoOff(cron)
