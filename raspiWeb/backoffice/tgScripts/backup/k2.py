#!/usr/bin/python

import globalVars
import sys


def kodiPlay(piNumber, sendFile):
    globalVars.redisRequestSet(
        globalVars.redisKodiRequest.replace('X', piNumber))
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "Kodi" + piNumber + " Starting")

if __name__ == "__main__":
    piNumber = __file__.replace('.py', '')[-1:]
    try:
        piNumber = int(piNumber)
    except Exception as e:
        try:
            piNumber = int(sys.argv[1])
        except Exception as e:
            piNumber = 0
    kodiPlay(str(piNumber), True)
