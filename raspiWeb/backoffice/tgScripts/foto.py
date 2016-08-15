#!/usr/bin/python

import globalVars
import sys


def photoRequest(piNumber=0):
    if piNumber == 0:
        for i in range(1, globalVars.numRaspis + 1):
            globalVars.redisRequestSet(
                globalVars.redisPhotoRequest.replace('X', str(i)))
    else:
        globalVars.redisRequestSet(
            globalVars.redisPhotoRequest.replace('X', str(piNumber)))

if __name__ == "__main__":
    try:
        piNumber = int(sys.argv[1])
    except Exception as e:
        piNumber = 0
    photoRequest(piNumber)
