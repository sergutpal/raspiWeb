# -*- coding: utf-8 -*-

import globalVars
import sys

if __name__ == "__main__":
    if (globalVars.setAlarmValue(globalVars.pathAlarmDB, globalVars.SQL_ALARM_UPDATE, 'alarmActive', globalVars.NIGHTMODE)):
        globalVars.toFile(globalVars.sendFile, "Modo noche activado")
    else:
        globalVars.toFile(globalVars.sendFile,
                          "No se ha podido actualizar el estado de la alarma!")