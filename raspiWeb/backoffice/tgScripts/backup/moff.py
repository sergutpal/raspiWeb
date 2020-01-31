#!/usr/bin/python

import globalVars


def musicaOff(sendFile):
    globalVars.redisRequestSet(
        globalVars.redisMusicaOffRequest.replace('X', '0'))
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "Peticion Musica OFF")


if __name__ == "__main__":
    musicaOff(True)
