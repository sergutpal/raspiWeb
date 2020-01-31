#!/usr/bin/python

import globalVars
import sys


def cameraStartRequest(piNumber=0):
    if piNumber == 0:
        for i in range(0, globalVars.numRaspis + 1):
            globalVars.redisRequestSet(
                globalVars.redisCameraStartRequest.replace('X', str(i)))
    else:
        globalVars.redisRequestSet(
            globalVars.redisCameraStartRequest.replace('X', str(piNumber)))
    globalVars.toFile(globalVars.sendFile, "Peticion iniciar camaras en modo video")


if __name__ == "__main__":
    try:
        piNumber = int(sys.argv[1])
    except Exception as e:
        piNumber = 0
    cameraStartRequest(piNumber)
