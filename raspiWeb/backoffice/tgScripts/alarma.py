# -*- coding: utf-8 -*-

import globalVars

if (globalVars.setAlarm(True)):
    globalVars.toFile(globalVars.sendFile, "Alarma ACTivada alarma.py")
else:
    globalVars.toFile(globalVars.sendFile,
                      "No se ha podido actualizar el estado de la alarma!")
