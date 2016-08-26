#!/usr/bin/python

import globalVars
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) >=2 and sys.argv[1].lower() =='cron':
        # Si el parametro es cron, quiere decir que la peticion viene de la tarea del cron y 
        # hay que comprobar si el modo auto del cron esta activo en la BD config. 
        if globalVars.getConfigField('alarmCronAutoActive') =='0':
            sys.exit(0)
    path, fileName = os.path.split(sys.argv[0])
    if (fileName.lower() =='auto.py'):
        active = True
        msg = 'Alarma en modo Automatico'
    else:
        active = False
        msg = 'Alarma: modo auto desactivado'
    if (globalVars.setAlarmAuto(active)):
        globalVars.toFile(globalVars.sendFile, msg)
    else:
        globalVars.toFile(globalVars.sendFile,
                          "No se ha podido actualizar el estado de la alarma!")
