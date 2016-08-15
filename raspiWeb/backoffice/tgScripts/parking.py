#!/usr/bin/python

import globalVars
import sys


def parkingRequest(waitSeconds='0'):
    globalVars.redisRequestSet(globalVars.redisParkingRequest, waitSeconds)
    globalVars.toFile(globalVars.sendFile,
                      "Abriendo parking en " + waitSeconds + " segundos")

if __name__ == "__main__":
    try:
        waitSeconds = int(sys.argv[1])
    except Exception as e:
        waitSeconds = 0
    waitSeconds = str(waitSeconds)
    parkingRequest(waitSeconds)
