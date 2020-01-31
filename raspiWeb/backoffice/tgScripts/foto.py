#!/usr/bin/python

import globalVars
import subprocess
import sys


def photoRequest(piNumber=0):
    if piNumber == 0:
        for i in range(0, globalVars.numRaspis + 1):
            globalVars.redisRequestSet(
                globalVars.redisPhotoRequest.replace('X', str(i)))
    else:
        globalVars.redisRequestSet(
            globalVars.redisPhotoRequest.replace('X', str(piNumber)))


def photoFFMPEG(URL, filename):
    try:
        command = '/usr/bin/ffmpeg -y -i ' + URL + ' -vframes 1 ' + filename
        subprocess.Popen(command, shell=True)
        return True
    except Exception as e:
        globalVars.toLogFile('Error photoFFMPEG: ' + str(e))
        return False


def photoEntrada():
    photoFFMPEG(globalVars.rtspEntrada, globalVars.pathTmpTelegram + 'entrada.jpg')


def photoSalon():
    photoFFMPEG(globalVars.rtspSalon,  globalVars.pathTmpTelegram + 'salon.jpg')


def photoWebCams():
    photoEntrada()
    photoSalon()


if __name__ == "__main__":
    try:
        piNumber = int(sys.argv[1])
    except Exception as e:
        piNumber = 0
    photoRequest(piNumber)
    photoWebCams()
