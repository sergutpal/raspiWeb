#!/usr/bin/python

import globalVars
import subprocess
import shutil
import time
import sys
from _thread import start_new_thread

def videoRequest(piNumber=0):
    if piNumber == 0:
        for i in range(0, globalVars.numRaspis + 1):
            if (i != 1):
                globalVars.redisRequestSet(
                    globalVars.redisVideoRequest.replace('X', str(i)))
    else:
        globalVars.redisRequestSet(
            globalVars.redisVideoRequest.replace('X', str(piNumber)))


def videoFFMPEG(URL, filename):
    try:
        filename = filename + globalVars.getUniqueIdFromDate() + '.mp4'
        command = '/usr/bin/ffmpeg -i ' + URL + ' -t ' + str(globalVars.timeVideoRecord) + ' -acodec copy -vcodec copy ' + globalVars.pathTmp + filename
        globalVars.toLogFile('Ejecutando: ' + command)
        subprocess.Popen(command, shell=True)
        time.sleep(globalVars.timeVideoRecord + 10)
        shutil.move(globalVars.pathTmp + filename, globalVars.pathDropBoxFromVideo + filename)
        return True
    except Exception as e:
        globalVars.toLogFile('Error videoFFMPEG: ' + str(e))
        return False


def videoEntrada():
    videoFFMPEG(globalVars.rtspEntrada, 'entrada')


def videoSalon():
    videoFFMPEG(globalVars.rtspSalon, 'salon')


def videoSotano():
    videoFFMPEG(globalVars.rtspSotano, 'sotano')


def videoTerraza():
    videoFFMPEG(globalVars.rtspTerraza, 'terraza')


def videoWebCams():
    try:
        videoSalon()
        videoEntrada()
        videoSotano()
        ## videoTerraza()
    except Exception as e:
        globalVars.toLogFile('Error videoWebCams: ' + str(e))
        return False



if __name__ == "__main__":
    try:
        piNumber = int(sys.argv[1])
    except Exception as e:
        piNumber = 0
    globalVars.toFile(globalVars.sendFile, 'Recibida la solicitud para grabar videos ' + str(globalVars.timeVideoRecord) + '(s). Los videos estarán disponibles en Dropbox.')
    videoRequest(piNumber)
    videoWebCams()


