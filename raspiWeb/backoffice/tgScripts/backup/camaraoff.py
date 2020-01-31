#!/usr/bin/python

import globalVars
import camara
import sys


def cameraOffRequest(piNumber=0):
    if piNumber == 0:
        for i in range(0, globalVars.numRaspis + 1):
            globalVars.redisRequestSet(
                globalVars.redisCameraOffRequest.replace('X', str(i)))
    else:
        globalVars.redisRequestSet(
            globalVars.redisCameraOffRequest.replace('X', str(piNumber)))


if __name__ == "__main__":
    try:
        piNumber = int(sys.argv[1])
    except Exception as e:
        piNumber = 0
    cameraOffRequest(piNumber)
    globalVars.toFile(globalVars.sendFile, "Solicitud apagar camaras")
