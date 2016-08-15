#!/usr/bin/python

import globalVars

if (globalVars.setAlarm(False)):
    globalVars.toFile(globalVars.sendFile, "Alarma desactivada")
else:
    globalVars.toFile(globalVars.sendFile,
                      "No se ha podido actualizar el estado de la alarma!")
