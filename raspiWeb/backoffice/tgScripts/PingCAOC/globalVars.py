#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import re
import socket

# En esta variable indicamos cuantas raspis tenemos para los bucles de
# peticion (solicitar temperatura, foto, tv, etc.)
numRaspis = 4
pathTmp = '/home/tmp/'
pathDropBoxFrom = pathTmp + 'dropbox/'
pathDropBoxFromPing = pathDropBoxFrom + 'ping/'
pathDropBoxFromBackup = pathDropBoxFrom + 'backup/'
pathDropBoxTo = '/cubieSrv/'
pathDropBoxToPing = pathDropBoxTo + 'ping/'
pathDropBoxToBackup = pathDropBoxTo + 'backup/'
pathDropBoxRead = pathDropBoxFrom + 'read/'
PINGFILE = 'ping.txt'
redisDropBoxIsBusy = 'dropboxIsBusy'
pathTmpTelegram = '/home/tmp/telegram/'
pathBase = '/home/nfs/'
pathBaseTelegram = pathBase + 'telegram/'
pathBaseTgScripts = pathBaseTelegram + 'tgScripts/'
pathNFS = pathBaseTelegram + 'enviado/'
pathConfigDB = pathBaseTelegram + 'db/config.db'
pathEfergyDB = pathTmpTelegram + 'efergy.db'
pathAlarmDB = pathBaseTelegram + 'db/alarma.db'
pathTemperatureDB = pathTmpTelegram + 'temperaturaraspiX.db'
pathParkingDB = pathBaseTelegram + 'db/parking.db'
logFile = 'log.txt'
alertFile = pathBaseTelegram + 'logs/logAlerts.txt'
redisAlarmRequest = 'AlarmRequestX'
redisAlarmMotionRequest = 'AlarmMotionRequestX'
redisMotionFirstMinuteIgnore = 'MotionIgnoreFirstMinuteX'
redisTempetureInsertRequest = 'insertTemperaturaX'
RpiCamPathTmp = pathTmpTelegram + 'RpiCam/'
RpiCamStarted = False
pathRpiCamFIFO = '/var/www/cam/FIFO'
pathRpiCamJPG = '/dev/shm/mjpeg/cam.jpg'
pathPhoto = pathTmpTelegram + 'RpiCam/RaspiX.jpg'
redisParkingRequest = 'openParking'
redisPhotoRequest = 'insertFotoX'
redisTVOffRequest = 'insertTVOffX'
redisTVOnRequest = 'insertTVOnX'
redisAlarmOffRequest = 'alarmOffX'
redisAlarmOffRequestCubie = 'alarmOffCubie'
redisAlarmSetRequest = 'alarmSetX'
redisRebootRequest = 'rebootX'
redisWatchdogRequest = 'watchdogX'
pathAlarmaMP3 = pathBase + 'mp3/alarma.mp3'
pathTVOn = pathBase + 'mp3/alarma.mp3'
redisMP3StreamingRequest = 'mp3StreamingX'
redisKodiRequest = 'KodiRequestX'
redisMusicaRequest = 'MusicaRequestX'
redisMusicaRestartRequest = 'MusicaRestartRequest'
redisMusicaOffRequest = 'MusicaOffRequestX'
redisPingRequest = 'PingRequestX'
redisPingTimeoutKO = 'PingTimeoutKO'
sendFile = pathTmpTelegram + 'send.txt'
sendFileToAll = pathTmpTelegram + 'sendAll.txt'
redisPhoneAlarmRequest = 'sendPhoneAlarm'
redisAlarmaYaAvisadaCubie = 'alarmaYaAvisadaCubie'
redisAlarmaYaAvisadaRaspi = 'alarmaYaAvisadaRaspiX'
tgDestination = 'Sergio'
tgDestinationAll = 'Casa'
MAX_CPU_TEMP_ALERT = 80.0
# La alerta de temperatura de CPU se enviara por telegram como maximo cada
# 10 minutos
MAX_SECONDS_ALERT_TEMP_CPU = 600
DATETIME_NOW = "datetime('now', 'localtime')"
DATETIME_TODAY = "datetime('now', 'localtime', 'start of day')"
DATETIME_LAST_HOUR = "datetime('now', 'localtime', '-1 hour')"
DATETIME_LAST_24H = "datetime('now', 'localtime', '-1 day')"
DATETIME_LAST_2HOUR = "datetime('now', 'localtime', '-2 hour')"
ACTIVE = '1'
INACTIVE = '0'
SQL_ALARM_SELECT = 'SELECT activa FROM alarma;'
SQL_ALARM_UPDATE = 'INSERT INTO historicoAlarma(activa, data) VALUES ' + \
    '(valor,' + DATETIME_NOW + ' );'
SQL_AUTO_UPDATE = 'UPDATE config SET alarmAuto = valor;'
SQL_GET_LAST = 'SELECT column, data FROM table;'
SQL_SELECT_HISTORY = 'SELECT COUNT(*) AS NumTotal, MAX(column) AS Maximo, ' + \
    'MIN(column) as Minimo, AVG(column) as Media ' + \
    'FROM historyTable WHERE data BETWEEN data1 AND data2;'
SQL_CONFIG_GET_FIELD = 'SELECT field FROM config;'
fileLog = None
mp3Cmd = 'mpg123'
kodiCmd = 'kodi'
SPACE_SEPARATOR = 100
djangoIPAuth = ''
raspiId = 0
raspiName = 'raspiX'


def dateTime():
    return time.strftime('%d/%m/%y %H:%M:%S ')


def flushSync(file, close):
    try:
        file.flush()
        try:
            os.fsync(file.fileno())
        except Exception as e:
            # Ignoramos la excepcion: las pipes no permiten estan operacion y
            # por eso generan una excepcion!
            # print 'Excepcion fsync: ' + str(e)
            pass
        if close:
            file.close()
    except Exception as e:
        toLogFile('Error flushSync: ' + str(e))
    return


def openLogFile():
    global logFile
    global fileLog

    if fileLog is None:
        fileLog = open(logFile, 'a')
        # fileLog.write('*******************************************\n')
        # fileLog.write(dateTime() + ' Inicio servicio envio Telegram \n')
        # fileLog.write('******************************************* \n')
        # flushSync(fileLog, False)
    return fileLog


def toLogFile(txt):
    global raspiName

    try:
        fileLog = openLogFile()
        fileLog.write(dateTime() + ' - ' + raspiName + '. ' + txt + '\n')
        flushSync(fileLog, False)
    except Exception as e:
        print('Error toLogFile: ' + str(e) + '\n')
    return
