#!/usr/bin/python

import globalVars

if (globalVars.setAlarmAuto(False)):
    globalVars.toFile(globalVars.sendFile, "Alarma: modo auto desactivado")
else:
    globalVars.toFile(globalVars.sendFile,
                      "No se ha podido actualizar el estado de la alarma!")
