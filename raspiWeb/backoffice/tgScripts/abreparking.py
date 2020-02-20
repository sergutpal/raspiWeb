#!/usr/bin/python

import globalVars
import sys


def parkingRequest(waitSeconds='0'):
    try:
        if globalVars.getConfigField('blockParking') == '1':
            globalVars.toLogFile('parkingRequest: peticion ignorada porque blockParking esta activado')
            return False

        if globalVars.isAlarmActive():
            if (globalVars.setAlarm(False)):
                globalVars.toFile(globalVars.sendFile, "Alarma desactivada")

        globalVars.redisRequestSet(globalVars.redisParkingRequest, waitSeconds)
        globalVars.toFile(globalVars.sendFile,
                          "Abriendo parking en " + waitSeconds + " segundos")
        return True
    except Exception as e:
        globalVars.toLogFile('Error parkingRequest: ' + str(e))
        return False


if __name__ == "__main__":
    globalVars.toLogFile('Peticions abrePparking recibida')
    try:
        waitSeconds = int(sys.argv[1])
    except Exception as e:
        waitSeconds = 0
    waitSeconds = str(waitSeconds)
    parkingRequest(waitSeconds)
