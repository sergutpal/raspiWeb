#!/usr/bin/python

import globalVars
import time
import sys


def getTemperatureHumidity():
    globalVars.getValues(globalVars.pathTemperatureDB.replace('X', '1'),
                         'TEMPERATURA SALON', 'temperatura',
                         'historicoTemperatura', 'temperatura', 'C',
                         globalVars.sendFileToAll)
    time.sleep(2)
    globalVars.getValues(globalVars.pathTemperatureDB.replace('X', '3'),
                         'TEMPERATURA DORMITORIO', 'temperatura',
                         'historicoTemperatura', 'temperatura', 'C',
                         globalVars.sendFileToAll)
    time.sleep(2)
    globalVars.getValues(globalVars.pathTemperatureDB.replace('X', '4'),
                         'TEMPERATURA PASILLO', 'temperatura',
                         'historicoTemperatura', 'temperatura', 'C',
                         globalVars.sendFileToAll)
    time.sleep(2)
    # globalVars.getValues(globalVars.pathTemperatureDB.replace('X', '2DHT22'),
    #                      'HUMEDAD CALLE', 'temperatura',
    #                     'historicoTemperatura', 'humedad', '%',
    #                     globalVars.sendFileToAll)
    # time.sleep(2)
    globalVars.getValues(globalVars.pathTemperatureDB.replace('X', '2DHT22'),
                         'TEMPERATURA CALLE DHT22', 'temperatura',
                         'historicoTemperatura', 'temperatura', 'C',
                         globalVars.sendFileToAll)
    # time.sleep(1)
    # globalVars.getValues(globalVars.pathTemperatureDB.replace('X','2'),
    # 'TEMPERATURA CALLE BMP180', 'temperatura', 'historicoTemperatura',
    # 'temperatura', 'C', globalVars.sendFileToAll)
    return True


def sendTemperatureRequest(piNumber=0):
    if piNumber == 0:
        for i in range(1, globalVars.numRaspis + 1):
            globalVars.redisRequestSet(
                globalVars.redisTempetureInsertRequest.replace('X', str(i)))
    else:
        globalVars.redisRequestSet(
            globalVars.redisTempetureInsertRequest.replace('X', str(piNumber)))
    return True


if __name__ == "__main__":
    try:
        piNumber = int(sys.argv[1])
    except Exception as e:
        piNumber = 0
    if sendTemperatureRequest(piNumber):
        time.sleep(5)
        getTemperatureHumidity()
