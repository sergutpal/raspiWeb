#!/usr/bin/python

import globalVars
import os
import sys

def setAlarmAutoOn(cron):
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
    try:
        cron = len(sys.argv) >=2 and sys.argv[1].lower() =='cron'
    except Exception as e:
        cron = False

    setAlarmAutoOn(cron)
