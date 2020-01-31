#!/usr/bin/python

import globalVars

def setAlarmOff():
    if (globalVars.setAlarm(False)):
        globalVars.toFile(globalVars.sendFile, "Alarma desactivada")
    else:
        globalVars.toFile(globalVars.sendFile,
                          "No se ha podido actualizar el estado de la alarma!")

if __name__ == "__main__":
    setAlarmOff()
