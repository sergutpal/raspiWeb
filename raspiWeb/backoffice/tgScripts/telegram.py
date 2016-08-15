#!/usr/bin/python

import os
import time
from datetime import datetime
import subprocess
import shutil
import globalVars
import thread
import sendmail
# from pycall import CallFile, Call, Application

hostname = globalVars.raspiName
ncCommand = 'nc 127.0.0.1 8009'
SECONDS_WAIT = 0.5
datetimeMaxTempCPU = None


def sendToNC(cmd):
    global ncCommand
    try:
        globalVars.toLogFile('Mensaje a enviar (nc): @' + cmd + '@')
        nc = subprocess.Popen(ncCommand, shell=True,
                              stdin=subprocess.PIPE, stdout=globalVars.fileLog)
        nc.stdin.write(cmd)
        nc.stdin.write('safe_quit')
        return None
    except Exception as e:
        globalVars.toLogFile('Error sendToNC: ' + str(e))
        return None


def checkPhoneAlarm():
    try:
        message = globalVars.redisGet(
            globalVars.redisPhoneAlarmRequest, True)  # Eliminamos el mensaje
        if message:
            # Enviamos el aviso de alarma por Telegram
            sendToNC('msg ' + globalVars.tgDestinationAll + ' ' + message)
            mailTo = globalVars.getConfigField('mail')
            if mailTo:
                sendmail.send_mail(
                    mailTo, 'Alarma importante en casa!', None, message)
            # Solo hacemos una llamada de alarma cada 10 minutos como maximo
            previousCall = globalVars.redisGet(
                globalVars.redisAlarmaYaAvisadaCubie, False)
            if previousCall is None:
                globalVars.redisSet(
                    globalVars.redisAlarmaYaAvisadaCubie, message, 600)
                for i in range(1, 4):
                    callPhone = globalVars.getConfigField('phone' + str(i))
                    if callPhone:
                        globalVars.callPhone(callPhone)
                        time.sleep(5)  # Esperamos 5s entre cada llamada
                # Play alarma.mp3
                globalVars.playMP3(globalVars.pathAlarmaMP3, False)
        return None
    except Exception as e:
        globalVars.toLogFile('Error checkPhoneAlarm: ' + str(e))
        return None


def checkMessage():
    sendMessage(globalVars.tgDestinationAll, globalVars.sendFileToAll, False)
    time.sleep(SECONDS_WAIT)
    sendMessage(globalVars.tgDestination, globalVars.sendFile, False)
    return None


def sendMessage(tgDestination, file, sendAlarm):
    try:
        fileTelegram = file
        if globalVars.fileIsAvailable(fileTelegram) and os.path.isfile(
                                                                fileTelegram):
            globalVars.getTelegramTo()  # Refrescamos los destinatarios
                                        # del mensaje Telegram
            message = globalVars.fromFile(fileTelegram)
            os.remove(fileTelegram)
            sendToNC('msg ' + tgDestination + ' ' + message)
        return
    except Exception as e:
        globalVars.toLogFile('Error sendMessage: ' + str(e))
        return


def sendMedia(cmd, ext, tgDestination, pathTmp, pathNFS):
    try:
        files = globalVars.filesByExt(pathTmp, ext)
        for file in files:
            pathNFSFile = globalVars.moveFromTmpToVar(file, pathTmp, pathNFS)
            if pathNFSFile is not None:
                # Importante: telegram-cli no envia el fichero si no se incluye
                # el salto de linea
                sendToNC(cmd + ' ' + tgDestination + ' ' + pathNFSFile + '\n')
            return
    except Exception as e:
        globalVars.toLogFile('Error sendMedia: ' + str(e))
        return


def checkCPUTemp():
    global hostname
    global datetimeMaxTempCPU
    maxSeconds = globalVars.MAX_SECONDS_ALERT_TEMP_CPU
    try:
        tempFile = open('/sys/class/thermal/thermal_zone0/temp')
        tempCPU = round(float(tempFile.read()) / 1000, 1)
        if (tempCPU > globalVars.MAX_CPU_TEMP_ALERT):
            msgAlert = globalVars.dateTime() + "ALERTA temperatura CPU " + \
                hostname + ": " + str(tempCPU)
            # globalVars.toFile(globalVars.alertCPUFile, msgAlert); #Se guarda
            # la alerta en el fichero de alertas de la temperatura de la CPU
            # La primera vez datetimeMaxTempCPU es None y debemos enviar a
            # telegram y registrar la alerta
            if (datetimeMaxTempCPU is None):
                numSeconds = globalVars.MAX_SECONDS_ALERT_TEMP_CPU + 1
            else:
                dateDiff = datetime.now() - datetimeMaxTempCPU
                numSeconds = dateDiff.total_seconds()
            # Solo enviamos alerta por Telegram si la temperatura ha subido
            # respecto el ultimo maximo
            if (numSeconds >= maxSeconds):
                # Se registra en el fichero global de alertas
                globalVars.toFile(globalVars.alertFile, msgAlert)
                # Se envia por Telegram
                globalVars.toFile(globalVars.sendFile, msgAlert)
                datetimeMaxTempCPU = datetime.now()
        return
    except Exception as e:
        globalVars.toLogFile('Error comprobando temperatura CPU: ' + str(e))
        return


def checkGlobalVarsValues():
    global SECONDS_WAIT

    SECONDS_WAIT = float(globalVars.getConfigField('checkSeconds'))
    #  globalVars.toLogFile(
    #    'checkGlobalVarsValues SECONDS_WAIT: ' + str(SECONDS_WAIT))
    globalVars.getTelegramTo()
    return


def checkPlayMP3():
    try:
        files = globalVars.filesByExt(globalVars.pathTmp, 'mp3')
        for file in files:
            if globalVars.fileIsAvailable(file):
                globalVars.playMP3(file, True)
    except Exception as e:
        globalVars.toLogFile('Error checkPlayMP3: ' + str(e))
    return


def moveRpiCamTmp():
    src = globalVars.RpiCamPathTmp
    try:
        for file in os.listdir(src):
            path = os.path.join(src, file)
            if globalVars.fileIsAvailable(path):
                if '.th.' not in path:
                    shutil.move(path, globalVars.pathTmp)
                else:
                    os.remove(path)
    except Exception as e:
        globalVars.toLogFile('Error moveRpiCamTmp: ' + str(e))
    return

checkGlobalVarsValues()
while (True):
    try:
        thread.start_new_thread(checkPhoneAlarm, ())
        thread.start_new_thread(globalVars.checkAlarmOffRequest, ())
        thread.start_new_thread(checkMessage, ())
        thread.start_new_thread(moveRpiCamTmp, ())
        thread.start_new_thread(sendMedia, ('send_photo', [
                  'png', 'gif', 'jpg'], globalVars.tgDestination,
                  globalVars.pathTmp, globalVars.pathNFS))
        thread.start_new_thread(sendMedia, ('send_video', ['mp4', 'mpg',
                                          'mpeg', 'mkv', 'avi'],
                                globalVars.tgDestination,
                                globalVars.pathTmp,
                                globalVars.pathNFS))
        thread.start_new_thread(checkPlayMP3, ())
        # thread.start_new_thread(checkCPUTemp, ())
        thread.start_new_thread(globalVars.flushSync,
                                (globalVars.fileLog, False))
        time.sleep(SECONDS_WAIT)
    except Exception as e:
        globalVars.toLogFile('Error procesando telegram.py: ' + str(e))
