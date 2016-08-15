#!/usr/bin/python

import globalVars

if (globalVars.setAlarmAuto(True)):
    globalVars.toFile(globalVars.sendFile, "Alarma en modo Automatico")
else:
    globalVars.toFile(globalVars.sendFile,
                      "No se ha podido actualizar el estado de la alarma!")
