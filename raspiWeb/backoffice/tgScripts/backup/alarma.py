# -*- coding: utf-8 -*-

import globalVars
import sys


def setAlarmOn(cmd):
    if (globalVars.setAlarm(True)):
        globalVars.toLogFile("Alarma ACTivada por ejecución de: " + cmd)
        globalVars.toFile(globalVars.sendFile, "Alarma ACTivada: " + cmd)
    else:
        globalVars.toFile(globalVars.sendFile,
                          "No se ha podido actualizar el estado de la alarma!")


if __name__ == "__main__":
    setAlarmOn(str(sys.argv))
