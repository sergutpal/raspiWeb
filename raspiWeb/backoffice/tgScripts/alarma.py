# -*- coding: utf-8 -*-

import globalVars
import sys

if __name__ == "__main__":
    if (globalVars.setAlarm(True)):
	globalVars.toLogFile("Alarma ACTivada por ejecución de: " + str(sys.argv))	
        globalVars.toFile(globalVars.sendFile, "Alarma ACTivada: " + str(sys.argv))
    else:
        globalVars.toFile(globalVars.sendFile,
                          "No se ha podido actualizar el estado de la alarma!")
