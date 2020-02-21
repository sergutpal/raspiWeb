#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este modulo recibe todas las peticiones de etiquetas NFC.
# Antes de ejecutar el comando hace las siguientes comprobaciones
# 1-) Que el comando tenga el formato valido sgp.comando#parametrosOpcionalesSeparadospor#.androidID.fechaHora_ddMMyyyy_HHmmss
# 2-) Que la fechaHora del comando recibido tenga una antiguedad como maximo de MAX_DELAY_CMD segundos
# 3-) Que no se haya recibido otro comando NFC con una anterioridad de REPEAT_CMD_SECONDS segundos

# Ejemplos de comandos NFC que hay que grabar en las tags
#       sgp.parking         Abrir parking de forma inmediata
#       sgp.parking#60      Abrir el parking en 60 segundos
#       sgp.kodi#3          Ejecutar Kodi3
#       sgp.m               Encender la musica


import globalVars
import time
import subprocess
import sys
import sqlite3


CMD_TEST_OK = "sgp"
MAX_DELAY_CMD = 30          # Si pasan más de MAX_DELAY_CMD segundos desde la recepción del mensaje, lo ignoramos
REPEAT_CMD_SECONDS = 2     # Si llegan nuevos mensajes dentro de los REPEAT_CMD_SECONDS del mensaje anterior procesado, los ignoramos 
SQL_ALARM_SELECT = 'SELECT COUNT(*) FROM androidAuthNFC WHERE androidID ="ANDROID_ID_XXXX";'


def checkNFCBlock():
    try:
        if globalVars.getConfigField('blockNFC') == '1':
            globalVars.toLogFile('checkNFCBlock: peticion NFC ignorada porque blockNFC esta activado')
            return True
        else:
            return False
    except Exception as e:
        globalVars.toLogFile('Error checkNFCBlock: ' + str(e))
        return False



def checkNFCFree():
    # Esta funcion comprueba que no hayan llegado 2 comandos NFC muy seguidos. En ese caso entendemos que
    # puede deberse a una segunda lectura demasiado rapida y en ese caso ignoramos la segunda cmd
    if not globalVars.redisGet(globalVars.redisNFCIsBusy, False):
        return True
    else:
        globalVars.toLogFile('checkNFCFree: Se ha ejecutado un comando NFC hace muy pocos segundos. Ignoramos esta petición')
        return False


def checkAndroidID(androidID):
    sql = SQL_ALARM_SELECT.replace('ANDROID_ID_XXXX', androidID)
    try:
        configDB = sqlite3.connect(globalVars.pathConfigDB)
        cur = configDB.cursor()
        cur.execute(sql)
        data = cur.fetchone()
        value = data[0]
        ret = value > 0
    except Exception as e:
        globalVars.toLogFile('Error checkAndroidID: ' + str(e))
        ret = False
    finally:
        cur.close()
        configDB.close()
        return ret
    return True


def execCMD(cmd):
    try:
        command = 'python3 ' + globalVars.pathBaseTgScripts + cmd
        subprocess.Popen(command, shell=True)
        globalVars.redisSet(globalVars.redisNFCIsBusy, command, REPEAT_CMD_SECONDS)
        globalVars.toLogFile('NFC: ' + command)
        return True
    except Exception as e:
        globalVars.toLogFile('Error execCMD: ' + str(e))
        return False


def parseExecNFC(cmd):
    try:
        c = cmd.split('.')

        if c[0] != CMD_TEST_OK:
            globalVars.toLogFile('parseExecNFC comando no reconocido: ' + cmd)
            return False

        cmdTime = time.strptime(c[3], '%d%m%Y_%H%M%S')
        now = time.localtime()
        secondsDiff = abs(time.mktime(now) - time.mktime(cmdTime))
        if secondsDiff > MAX_DELAY_CMD:
            globalVars.toLogFile('parseExecNFC han pasado mas de ' + str(MAX_DELAY_CMD) + ' segundos. Comando: ' + cmd + ' ignorado')
            return False

        androidID = c[2]
        # Comprobamos que el dispositivo que ha enviado el comando sea un dispositivo autorizado
        if not checkAndroidID(androidID):
            globalVars.toLogFile('parseExecNFC han pasado mas de ' + str(MAX_DELAY_CMD) + ' segundos. Comando: ' + cmd + ' ignorado')
            return False

        space = ' '
        cmd = c[1].replace('#', space)  # El comando a ejecutar puede llevar parametros que separamos por #
        cmd = cmd.split(space)
        cmd[0] = cmd[0] + '.py'  # Anyadimos el .py al comando a ejecutar (debe ser siempre un comando python)
        cmd = space.join(cmd)
        execCMD(cmd)

        return True
    except Exception as e:
        globalVars.toLogFile('Error parseExecNFC: ' + str(e))
        return False


if __name__ == "__main__":
    try:
        if len(sys.argv) >=2:
            cmd = sys.argv[1]
            if not checkNFCBlock() and checkNFCFree():
                parseExecNFC(cmd)
    except Exception as e:
        globalVars.toLogFile('Error NFC: ' + str(e))
