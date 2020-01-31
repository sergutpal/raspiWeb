#!/usr/bin/python

import sys
import globalVars


def musicaPlay(restartMPD, sendFile):
    if restartMPD:
        globalVars.redisRequestSet(globalVars.redisMusicaRestartRequest)
    globalVars.redisRequestSet(
        globalVars.redisMusicaRequest.replace('X', '0'))
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "Peticion Musica ON")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        restartMPD = True
    else:
        restartMPD = False
    musicaPlay(restartMPD, True)
