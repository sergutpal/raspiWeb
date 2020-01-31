#!/usr/bin/python

import globalVars
import sys
import time


# Funcion que llamara cubieSrv desde un cron para comprobar si las raspis estan ok
def sendPingRequest(piNumber=0):
    try:
        if piNumber == 0:
            for i in range(1, globalVars.numRaspis + 1):
                if (i != 2):
                    pingRequest = globalVars.redisPingRequest.replace('X', str(i))
                    globalVars.redisSet(pingRequest, pingRequest, 240)
        else:
            pingRequest = globalVars.redisPingRequest.replace('X', str(piNumber))
            globalVars.redisSet(pingRequest, pingRequest)
        # fechahora = time.gmtime()
        fechahora = time.localtime()
        fechahora = time.strftime("%d/%m/%Y %H:%M:%S", fechahora)
        globalVars.redisSet(globalVars.redisPingTimeoutKO, fechahora)
        return True
    except Exception as e:
        globalVars.toLogFile('Error sendPingRequest: ' + str(e))
    return False


# Funcion que debe llamar cubieSrv en telegram.py
def checkPingReply():
    try:
        pingTimeStr = globalVars.redisGet(globalVars.redisPingTimeoutKO, False)
        if pingTimeStr:
            pingTime = time.strptime(pingTimeStr, '%d/%m/%Y %H:%M:%S')
            # now = time.gmtime()
            now = time.localtime()
            secondsDiff = time.mktime(now) - time.mktime(pingTime)
            if secondsDiff > 120:
                # Se ha superado el tiempo para recibir respuesta de las raspis.
                # Hay que comprobar que todas las peticiones de ping esten ok
                msgNoPing = 'Ping test raspis: '
                KO = False
                for i in range(0, globalVars.numRaspis + 1):
                    pingPi = globalVars.redisPingRequest.replace('X', str(i))
                    if globalVars.redisRequestGet(pingPi):
                        msgNoPing = msgNoPing + 'Pi ' + str(i) + ' KO. '
                        KO = True
                if KO:
                    globalVars.toFile(globalVars.sendFile, msgNoPing)
                    # globalVars.toFile(globalVars.pathDropBoxFromPing, msgNoPing)
                # Eliminamos la entrada del ping
                globalVars.redisRequestGet(globalVars.redisPingTimeoutKO)
        return True
    except Exception as e:
        globalVars.toLogFile('Error checkPingReply: ' + str(e))
    return False


# Funcion que debe llamar cada una de las raspis en pir.py para responder el ping
def setPingReply(piNumber):
    pingRequest = globalVars.redisPingRequest.replace('X', str(piNumber))
    globalVars.redisDelete(pingRequest)
    return True


def updatePing():
    try:
        # fechaHora = time.gmtime()
        fechaHora = time.localtime()
        fechaHora = time.strftime('%d/%m/%Y %H:%M:%S', fechaHora)

        fileFromName = globalVars.PINGFILE
        fileFrom = globalVars.pathDropBoxFromPing + fileFromName
        globalVars.toFile(fileFrom, fechaHora, True, 'w')
        return True
    except Exception as e:
        globalVars.toLogFile('Error updatePing: ' + str(e))
    return False



if __name__ == "__main__":
    try:
        piNumber = int(sys.argv[1])
    except Exception as e:
        piNumber = 0
    sendPingRequest(piNumber)
    updatePing()
