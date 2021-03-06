#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import re
import socket
import sqlite3
import shutil
import psutil
from pycall import CallFile, Call, Context
import redis

# En esta variable indicamos cuantas raspis tenemos para los bucles de
# peticion (solicitar temperatura, foto, tv, etc.)
numRaspis = 4
redisSrv = redis.Redis("192.168.1.20", decode_responses=True)
pathTmp = '/home/tmp/'
pathDeleteLogic = '/home/nfs/tmp/ToDelete'
pathDropBoxFrom = pathTmp + 'dropbox/'
pathDropBoxFromPing = pathDropBoxFrom + 'ping/'
pathDropBoxFromBackup = pathDropBoxFrom + 'backup/'
pathDropBoxFromCamEntrada = pathDropBoxFrom + 'camEntrada/'
pathDropBoxFromCamComedor = pathDropBoxFrom + 'camComedor/'
pathDropBoxFromVideo = pathDropBoxFrom + 'video/'
pathDropBoxTo = '/cubieSrv/'
pathDropBoxToPing = pathDropBoxTo + 'ping/'
pathDropBoxToBackup = pathDropBoxTo + 'backup/'
pathDropBoxToCamEntrada = pathDropBoxTo + 'camEntrada/'
pathDropBoxToCamComedor = pathDropBoxTo + 'camComedor/'
pathDropBoxToVideo = pathDropBoxTo + 'video/'
pathDropBoxRead = pathDropBoxFrom + 'read/'
PINGFILE = 'ping.txt'
redisPuertaParkingAbierta = 'PuertaParkingAbierta'
redisLogSize = 'LogSize'
redisDropBoxIsBusy = 'dropboxIsBusy'
redisRTL433IsBusy = 'RTL433IsBusy'
redisNFCIsBusy = 'redisNFCIsBusy'
redisPVNow = 'PVNow'
redisPVSumToday = 'PVSumToday'
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
logFile = pathTmpTelegram + 'logs/log.txt'
alertFile = pathBaseTelegram + 'logs/logAlerts.txt'
redisAlarmRequest = 'AlarmRequestX'
redisTimbreRequest = 'TimbreRequestX'
redisAlarmMotionRequest = 'AlarmMotionRequestX'
redisMotionFirstMinuteIgnore = 'MotionIgnoreFirstMinuteX'
redisTempetureInsertRequest = 'insertTemperaturaX'
RpiCamPathTmp = pathTmpTelegram + 'RpiCam/'
RpiCamStarted = False
pathRpiCamFIFO = '/var/www/cam/FIFO'
pathRpiCamMedia = '/var/www/cam/media/'
pathRpiCamJPG = '/dev/shm/mjpeg/cam.jpg'
pathPhoto = pathTmpTelegram + 'RpiCam/RaspiX.jpg'
pathVideo = pathTmpTelegram + 'RpiCam/RaspiX.mp4'
pathAlexaTTS=pathBaseTgScripts +'alexaTTS/'
redisParkingRequest = 'openParking'
redisBombaAguaAutoOff = 'bombaAguaAutoOff'
redisBombaAguaNoAuto = 'bombaAguaNoAuto'
redisPhotoRequest = 'insertFotoX'
redisVideoRequest = 'insertVideoX'
redisCameraStartRequest = 'insertCameraStartX'
redisCameraOffRequest = 'redisCameraOffRequestX'
redisTVOffRequest = 'insertTVOffX'
redisTVOnRequest = 'insertTVOnX'
redisAlarmOffRequest = 'alarmOffX'
redisAlarmOffRequestCubie = 'alarmOffCubie'
redisAlarmSetRequest = 'alarmSetX'
redisRebootRequest = 'rebootX'
redisWatchdogRequest = 'watchdogX'
pathAlarmaMP3 = pathBase + 'mp3/alarma.mp3'
pathTimbreMP3 = pathBase + 'mp3/timbre.mp3'
pathParkingAbiertoMP3 = pathBase + 'mp3/parkingAbierto.mp3'
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
redisAlarmaBolsaYaAvisada = 'alarmaYaAvisadaBolsaX'
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
NIGHTMODE = '2'
SQL_ALARM_SELECT = 'SELECT activa FROM alarma;'
SQL_ALARM_UPDATE = 'INSERT INTO historicoAlarma(activa, data) VALUES ' + \
    '(valor,' + DATETIME_NOW + ' );'
SQL_AUTO_UPDATE = 'UPDATE config SET alarmAuto = valor;'
SQL_RADIOPARKING_UPDATE = 'UPDATE config SET radioParking = valor;'
SQL_SAVEVIDEOCAMS_UPDATE = 'UPDATE config SET saveVideoCams = valor;'
SQL_AUTOTERMO_UPDATE = 'UPDATE config SET autoTermo = valor;'
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
aqaraMotionNum = 4
aqaraDoorNum = 3
aqaraSmokeNum = 3
aqaraSOSAguaNum = 1
timeVideoRecord = 60
rtspEntrada = 'rtsp://admin:VTLOZG@192.168.1.74:554'
rtspSalon = 'rtsp://admin:KVHPVD@192.168.1.73:554'
rtspSotano = 'rtsp://admin:GMHANA@192.168.1.72:554'
rtspTerraza = 'rtsp://admin:WTUJDT@192.168.1.71:554'
raspiId = '0'
raspiName = 'raspiX'


def initGlobalVars():
    global raspiId
    global raspiName
    global djangoIPAuth

    raspiId = getRaspiId()
    raspiName = getHostName()
    openLogFile()
    getTelegramTo()
    djangoIPAuth = getConfigField('djangoIPAuth')
    return True


def isParkingOpen():
    global pathParkingDB

    try:
        parkingDB = sqlite3.connect(pathParkingDB)
        cur = parkingDB.cursor()
        cur.execute('SELECT open FROM parking')
        data = cur.fetchone()
        if (str(data[0]) == 1):
            return True
        else:
            return False
    except Exception as e:
        toLogFile('Error isParkingOpen ' + str(e) + '\n')
        return False


def isAlarmAuto():
    value = getConfigField('alarmAuto')
    if value is None:
        # Si no se ha podido recuperar el valor, entendemos que Auto es False
        return False
    else:
        if (value == ACTIVE):
            return True
        else:
            return False


def getAlarmValue():
    global pathAlarmDB
    global SQL_ALARM_SELECT

    try:
        alarmStatus = redisGet('alarmActive')
        if alarmStatus is not None:
            return alarmStatus

        alarmDB = sqlite3.connect(pathAlarmDB)
        cur = alarmDB.cursor()
        cur.execute(SQL_ALARM_SELECT)
        data = cur.fetchone()
        cur.close()
        alarmDB.close()
        value = str(data[0])

        redisSet('alarmActive', value)
        return value
    except Exception as e:
        toLogFile('Error getAlarmValue: ' + str(e))
        return False


def isNightModeActive():
    global NIGHTMODE

    try:
        value = getAlarmValue()
        if (value == NIGHTMODE):
            return True
        else:
            return False
    except Exception as e:
        toLogFile('Error isNightModeActive: ' + str(e))
        return False


def isAlarmActive():
    global ACTIVE
    global raspiId

    try:
        value = getAlarmValue()
        if (value == ACTIVE):
            return True
        else:
            if (raspiId != '3' and raspiId != '1'):  # En el modo noche, la unica Raspi que no debe estar "atenta" es la Raspi3. Tampoco Raspi1 que parece que está dando falsas alarmas
                return isNightModeActive()
            else:
                return False
    except Exception as e:
        toLogFile('Error isAlarmActive: ' + str(e))
        return False


def setAlarmValue(pathDB, sql, field, value):
    global ACTIVE
    global INACTIVE
    global NIGHTMODE
    global redisAlarmSetRequest
    global numRaspis

    try:
        if (value == NIGHTMODE):
            alarmStatus = NIGHTMODE
        else:
            if (value):
                alarmStatus = ACTIVE
            else:
                alarmStatus = INACTIVE
        redisSet(field, alarmStatus)
        sqlExec = sql.replace('valor', alarmStatus)
        DB = sqlite3.connect(pathDB)
        cur = DB.cursor()
        cur.execute(sqlExec)
        DB.commit()
        cur.close()
        DB.close()
        if (field == 'alarmActive'):
            # Enviamos señal de cambio a todas las Pis para que
            # arranquen/paren motion+camara
            for i in range(1, numRaspis + 1):
                redisRequestSet(redisAlarmSetRequest.replace('X', str(i)))
                # Al iniciar el servicio Motion podemos tener falsas alarmas
                # Por eso enviamos señal para ignorar todas las posibles
                # detecciones del primer minuto
                redisSet(redisMotionFirstMinuteIgnore.replace('X', str(i)), 'Ignorar los eventos del primer minuto', 60)
        return True
    except Exception as e:
        toLogFile('Error setAlarmValue: ' + str(e))
        return False


def setAlarm(isActive):
    global SQL_ALARM_UPDATE
    global pathAlarmDB
    global numRaspis
    global redisAlarmOffRequestCubie
    global redisAlarmOffRequest

    if not isActive:
        for i in range(1, numRaspis + 1):
            redisRequestSet(redisAlarmOffRequest.replace('X', str(i)))
        redisRequestSet(redisAlarmOffRequestCubie)
    return setAlarmValue(pathAlarmDB, SQL_ALARM_UPDATE, 'alarmActive',
                         isActive)


def setAlarmAuto(isAuto):
    global SQL_AUTO_UPDATE
    global pathConfigDB

    return setAlarmValue(pathConfigDB, SQL_AUTO_UPDATE, 'configalarmAuto',
                         isAuto)


def checkAlarmOffRequest():
    global raspiId
    global mp3Cmd
    global kodiCmd

    try:
        killOk = False
        if ((raspiId == '0') and (redisRequestGet(redisAlarmOffRequestCubie))):
            killOk = True
        if ((raspiId != '0') and
                (redisRequestGet(redisAlarmOffRequest.replace('X', raspiId)))):
            killOk = True
        if killOk:
            killProcessByName(mp3Cmd)
            killProcessByName(kodiCmd)
            # Enviamos senyal para apagar la tv
            redisRequestSet(redisTVOffRequest.replace('X', '1'))
            redisRequestSet(redisTVOffRequest.replace('X', '3'))
        return None
    except Exception as e:
        toLogFile('Error checkAlarmOffRequest: ' + str(e))


def callPhone(phoneNumber):
    try:
        toLogFile('Peticion callPhone: ' + phoneNumber)
        sipNumber = 'SIP/' + phoneNumber + '@netelip'
        call = Call(sipNumber, callerid="Cubie Alarm",
                    wait_time=60, retry_time=60, max_retries=0)
        con = Context('alerta', 's', '1')
        cf = CallFile(call, con, archive=True)
        cf.spool()
        return phoneNumber
    except Exception as e:
        toLogFile('Error callPhone: ' + str(e))


def getHostName():
    return socket.gethostname()


def getRaspiId():
    raspi = getHostName()
    raspiN = raspi[-1:]
    if raspiN.isdigit():
        return raspiN
    else:
        return '0'  # Es la Cubie y la identificamos con el 0


def getTemperatureDBPath():
    global raspiId

    return pathTemperatureDB.replace('X', raspiId)


def dateTime():
    return time.strftime('%d/%m/%y %H:%M:%S ')


def flushSync(file, close):
    try:
        file.flush()
        try:
            os.fsync(file.fileno())
        except Exception as e:
            # Ignoramos la excepcion: las pipes no permiten esta operacion y
            # por eso generan una excepcion!
            # print('Excepcion fsync: ' + str(e))
            pass
        if close:
            file.close()
    except Exception as e:
        toLogFile('Error flushSync: ' + str(e))
    return


def toFile(filePath, txt, flush=True, mode='a'):
    try:
        # file = open(filePath, 'a+')
        file = open(filePath, mode)
        file.write(txt + '\n')
        if flush:
            flushSync(file, True)
    except Exception as e:
        toLogFile('Error toFile: ' + str(e))
    return


def fromFile(filePath):
    try:
        file = open(filePath, 'r')
        txt = file.read()
        file.close()
        return txt
    except Exception as e:
        toLogFile('Error fromFile: ' + str(e))
        return ''


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


def fileIsAvailable(filepath):
    available = None
    file_object = None
    if os.path.exists(filepath):
        try:
            file_object = open(filepath, 'a')
            if file_object:
                available = True
        except IOError:
            available = False
        finally:
            if file_object:
                file_object.close()
                return available
            else:
                return False


def fileExistsWaitIsAvailable(filepath):
    wait_seconds = 5
    retry = 0
    max_retry = 10

    while not fileIsAvailable(filepath) and (retry < max_retry):
        time.sleep(wait_seconds)
        retry = retry + 1

        if (retry < max_retry):
            return True
        else:
            return False


def moveFile(filepath, directory):
    fileName = os.path.basename(filepath)
    if os.path.exists(directory + '/' + fileName):
        os.remove(directory + '/' + fileName)
    shutil.move(filepath, directory)


def findProcess(processName):
    #ps = subprocess.Popen("ps -C " + processName,
    #                      shell=True, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)
    #output = ps.stdout.read()
    #ps.stdout.close()
    #ps.wait()
    #return output

    found = False
    try:
        processName = processName.lower()
        for proc in psutil.process_iter():
            procName = proc.name()
            procName = procName.lower()
            if processName in procName:
                proc.kill()
                found = True
        return found
    except Exception as e:
        toLogFile('Error findProcess: ' + str(e))
        return False


def isProcessRunning(processName):
    output = findProcess(processName)
    return output


def killProcessByName(processName):
    killed = False
    try:
        processName = processName.lower()
        for proc in psutil.process_iter():
            procName = proc.name()
            procName = procName.lower()
            if processName in procName:
                proc.kill()
                killed = True
        return killed
    except Exception as e:
        toLogFile('Error killProcessByName: ' + str(e))
        return False


def supervisor(cmd, start):
    global sendFile
    try:
        if start:
            action = ' start '
        else:
            action = ' stop '
        command = '/usr/bin/supervisorctl' + action + cmd
        subprocess.Popen(command, shell=True)
        return True
    except Exception as e:
        toLogFile('Error supervisor: ' + str(e))
        return False


def getConfigField(fieldName):
    global pathConfigDB
    global SQL_CONFIG_GET_FIELD

    try:
        value = redisGet('config' + fieldName)
        if value:
            # Si el valor esta en la cache (redis) se devuelve de alli, en caso
            # contrario se recoge de la BD
            return value
        configDB = sqlite3.connect(pathConfigDB)
        cur = configDB.cursor()
        sql = SQL_CONFIG_GET_FIELD.replace('field', fieldName)
        cur.execute(sql)
        data = cur.fetchone()
        value = str(data[0])
        cur.close()
        configDB.close()
        redisSet('config' + fieldName, value)
        return value
    except Exception as e:
        toLogFile('Error getConfigField ' + fieldName + ': ' + str(e))
        return ''


def getTelegramTo():
    global tgDestination
    global tgDestinationAll

    tgDestination = getConfigField('telegramTo')
    tgDestinationAll = getConfigField('telegramAll')
    return tgDestination


def getActualValue(cur, tableName, columnName, unityValue, allInOne=True):
    global SQL_GET_LAST

    sqlExec = SQL_GET_LAST.replace(
        'table', tableName).replace('column', columnName)
    cur.execute(sqlExec)
    row = cur.fetchone()
    if (allInOne):
        out = str(round(row[0], 1)) + unityValue + '. ' + row[1] + ' '
    else:
        t = row[1]  # El valor es una fecha + hora
        t = t[-8:]  # Nos quedamos unicamente con la hora
        out = {'value': str(round(row[0], 1)), 'time': t}
    return out


def getValues(pathDB, subject, tableName, historyTableName, columnName,
              unityValue, fileToSend):
    global SQL_SELECT_HISTORY
    global DATETIME_LAST_HOUR
    global DATETIME_NOW
    global SPACE_SEPARATOR

    try:
        DB = sqlite3.connect(pathDB)
        cur = DB.cursor()
        txtOut = subject + '. '
        value = getActualValue(cur, tableName, columnName, unityValue)
        txtOut = txtOut + 'Actual: ' + value
        sqlHistory = SQL_SELECT_HISTORY.replace(
            'historyTable', historyTableName).replace('column', columnName)
        sqlExec = sqlHistory.replace(
            'data1', DATETIME_LAST_HOUR).replace('data2', DATETIME_NOW)
        cur.execute(sqlExec)
        row = cur.fetchone()
        txtOut = txtOut + 'Ult. Hora. Count: ' + str(round(row[0], 1)) + \
            '. Maximo: ' + str(round(row[1], 1)) + unityValue + \
            '. Minimo: ' + str(round(row[2], 1)) + unityValue + \
            '. Media: ' + str(round(row[3], 1)) + unityValue + ' '
        txtOut = txtOut.ljust(len(txtOut) + SPACE_SEPARATOR)
        sqlExec = sqlHistory.replace(
            'data1', DATETIME_TODAY).replace('data2', DATETIME_NOW)
        cur.execute(sqlExec)
        row = cur.fetchone()
        txtOut = txtOut + 'Hoy. Count: ' + str(round(row[0], 1)) + \
            '. Maximo: ' + str(round(row[1], 1)) + unityValue + \
            '. Minimo: ' + str(round(row[2], 1)) + unityValue + \
            '. Media: ' + str(round(row[3], 1)) + unityValue + '\n'
        txtOut = txtOut.ljust(len(txtOut) + SPACE_SEPARATOR)
        toFile(fileToSend, txtOut)
        ret = True
    except Exception as e:
        toLogFile('Error getValues: ' + tableName + '. ' + columnName + str(e))
        ret = False
    finally:
        cur.close()
        DB.close()
        return ret


def moveFromTmpToVar(fileFrom, pathTmp, pathNFS):
    if (fileIsAvailable(fileFrom)):
        fileTo = fileFrom.replace(pathTmp, pathNFS)
        shutil.move(fileFrom, fileTo)
        return fileTo
    else:
        return None


def filesByExt(path, extList):
    filesExt = []
    for file in os.listdir(path):
        for ext in extList:
            ext = ext.lower()
            fileLower = file.lower()
            if fileLower.endswith(ext):
                filesExt.append(path + file)
                break
    return filesExt


def playMP3(pathMP3, deleteMP3, isAlarm=False):
    global mp3Cmd
    global raspiId

    if (((raspiId == '3') or (raspiId == '0')) and isAlarm):
        cmd = pathBaseTgScripts + 'pi3BTMP3.sh'
        #return True
    else:
        cmd = mp3Cmd + ' "' + pathMP3 + '"'

    try:
        if not isProcessRunning(mp3Cmd):
            #toLogFile('Reproduciendo MP3: ' + pathMP3)
            subprocess.Popen(cmd, shell=True, universal_newlines=True, bufsize=1)
            if deleteMP3:
                try:
                    time.sleep(10)
                    os.remove(pathMP3)
                except Exception as e:
                    toLogFile('Error deleteMP3: ' + str(e))
        return True
    except Exception as e:
        toLogFile('Error playMP3: ' + str(e))
        return False


def redisGet(key, clearKey=False):
    global redisSrv

    try:
        value = redisSrv.get(key)
        if (clearKey and value):
            redisSrv.delete(key)
        return value
    except Exception as e:
        toLogFile('redisGet Key: ' + key + '. ' + str(e))
        return None


def redisGetBool(key, clearKey=False):
    global ACTIVE

    value = redisGet(key, clearKey)
    if (value):
        # Hay valor en la cache (redis)
        if (str(value) == ACTIVE):
            return True
        else:
            return False
    else:
        return None


def redisSet(key, valor, secondsExpire=0):
    global redisSrv

    try:
        if (secondsExpire > 0):
            redisSrv.setex(name=key, value=valor, time=secondsExpire)
        else:
            redisSrv.set(key, valor)
        return True
    except Exception as e:
        toLogFile('redisSet Key: ' + key + '. ' + str(e))
        return None


def redisRequestSet(keyRequest, valueRequest=''):
    secondsExpire = 120
    if valueRequest == '':
        valueRequest = 'Peticion: ' + keyRequest
    return redisSet(keyRequest, valueRequest, secondsExpire)


def redisRequestGet(keyRequest):
    try:
        # Despues de la comprobacion, debemos eliminar la entrada para
        # reiniciar el circuito de peticiones
        existKey = redisGet(keyRequest, True)
        if existKey:
            return True
        else:
            return False
    except Exception as e:
        toLogFile('redisRequestGet Key: ' + keyRequest + '. ' + str(e))
        return None


def redisDelete(key):
    global redisSrv

    try:
        redisSrv.delete(key)
        return True
    except Exception as e:
        toLogFile('redisDelete Key: ' + key + '. ' + str(e))
        return None


def rebootNow():
    command = "/sbin/shutdown -r now"
    try:
        subprocess.Popen(command, shell=True)
    except Exception as e:
        txt = str(e)
        toLogFile('Error RebootNow: ' + txt)
    return True


def rebootRequest(sendToTelegram, piNumber='0'):
    global raspiId
    global numRaspis
    global sendFile
    global redisRebootRequest

    if piNumber == '0':
        for i in range(1, numRaspis + 1):
            redisRequestSet(redisRebootRequest.replace('X', str(i)))
        time.sleep(5)
        if sendToTelegram:
            toFile(sendFile, "Rebooting pi" + piNumber)
            time.sleep(2)
        rebootNow()
    else:
        redisRequestSet(redisRebootRequest.replace('X', piNumber))
    return True


def watchdogNow():
    command = "/usr/sbin/watchdog"
    try:
        subprocess.Popen(command, shell=True)
    except Exception as e:
        txt = str(e)
        toLogFile('Error WatchdogNow: ' + txt)
    return True


def watchdogRequest(sendToTelegram, piNumber='0'):
    global raspiId
    global numRaspis
    global sendFile
    global redisWatchdogRequest

    if piNumber == '0':
        for i in range(1, numRaspis + 1):
            redisRequestSet(redisWatchdogRequest.replace('X', str(i)))
        if sendToTelegram:
            toFile(sendFile, "Watchdog pi" + piNumber)
        watchdogNow()
    else:
        redisRequestSet(redisWatchdogRequest.replace('X', piNumber))


def fail2ban(action):
    global sendFile

    cmd = '/usr/bin/fail2ban-client '
    action = action.lower()
    if (action == 'on'):
        action = 'start'
    elif (action == 'off'):
        action = 'stop'
    else:
        action = 'status'
    try:
        cmd = cmd + action
        toLogFile('Cmd fail2ban: ' + cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)
        #txt = process.communicate()[0]
        txt = 'Desconocido'
        txt = 'Estado fail2ban: ' + txt
        toFile(sendFile, txt)
    except Exception as e:
        toLogFile('Error fail2ban: ' + str(e))


def firewall(action):
    global sendFile

    cmd = '/usr/sbin/ufw '
    action = action.lower()
    if (action == 'on'):
        action = 'enable'
    elif (action == 'off'):
        action = 'disable'
    else:
        action = 'status'
    try:
        cmd = cmd + action
        toLogFile('Cmd UFW: ' + cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True, bufsize=1)
        #txt = process.communicate()[0]
        #txt = 'Estado Firewall(UFW): ' + txt
        txt = 'Estado Firewall(UFW) desconocido'
        toFile(sendFile, txt)
    except Exception as e:
        toLogFile('Error firewall: ' + str(e))


def playMusic(sendTelegram):
    global sendFile
    global pathBaseTgScripts
    global redisMusicaRestartRequest

    if redisRequestGet(redisMusicaRestartRequest):
        restart = " restart"
    else:
        restart = ""

    command = pathBaseTgScripts + "musica.sh" + restart
    subprocess.Popen(command, shell=True)

    if sendTelegram:
        toFile(sendFile, "mpc PLAYing")
    return True


def stopMusic(sendTelegram):
    global sendFile

    #toLogFile('SGP llegando peticion mo')
    command = "/usr/bin/mpc stop -h 127.0.0.1"
    subprocess.Popen(command, shell=True)
    if (sendTelegram):
    	toFile(sendFile, "mpc STOP SGP")
    return True


def getUniqueIdFromDate():
    ts = time.localtime()
    ts = time.strftime("%d%m%Y_%H%M%S", ts)
    return ts


def playAlexaTTS(path):
    global raspiId
    global pathAlexaTTS

    if (raspiId != '0'):
        return None

    try:
        pathAlarmaTTS = pathAlexaTTS + path
        toLogFile('playAlexaTTS: ' + pathAlarmaTTS)
        subprocess.Popen(pathAlarmaTTS, shell=True, universal_newlines=True, bufsize=1)
        return True
    except Exception as e:
        toLogFile('Error playAlexaTTS: ' + str(e))
        return False


def fireAlarm(alerta):
    strAlert = dateTime() + raspiName + alerta + '\n'
    redisSet(redisPhoneAlarmRequest, strAlert)
    for i in range(0, numRaspis + 1):
        redisRequestSet(
            redisAlarmRequest.replace('X',str(i)))
    toFile(alertFile, strAlert)


def getLogSize():
    try:
        size = os.path.getsize(logFile)
        return str(size)
    except Exception as e:
        toLogFile('Error getLogSize: ' + str(e))
        return "0"


# Esta función se llama desde cron cada 1h
def setIniLogSize():
    sizeLogFile = getLogSize()
    redisSet(redisLogSize, sizeLogFile)


def setRadioParking(value):
    global pathConfigDB
    global SQL_RADIOPARKING_UPDATE
    global sendFile

    sql = SQL_RADIOPARKING_UPDATE
    try:
        redisSet('configradioParking', value)
        sqlExec = sql.replace('valor', value)
        DB = sqlite3.connect(pathConfigDB)
        cur = DB.cursor()
        cur.execute(sqlExec)
        DB.commit()
        cur.close()
        DB.close()
        # toFile(sendFile, "Radio Parking actualizado a " + value)
        return True
    except Exception as e:
        toLogFile('Error setRadioParking: ' + str(e))
        return False


def setRadioParkingOff():
    setRadioParking('0')


def setRadioParkingOn():
    setRadioParking('1')


def setSaveVideoCams(value):
    global pathConfigDB
    global SQL_SAVEVIDEOCAMS_UPDATE
    global sendFile

    sql = SQL_SAVEVIDEOCAMS_UPDATE
    try:
        redisSet('configsaveVideoCams', value)
        sqlExec = sql.replace('valor', value)
        DB = sqlite3.connect(pathConfigDB)
        cur = DB.cursor()
        cur.execute(sqlExec)
        DB.commit()
        cur.close()
        DB.close()
        toFile(sendFile, "saveVideoCams actualizado a " + value)
        return True
    except Exception as e:
        toLogFile('Error setSaveVideoCams: ' + str(e))
        return False


def setSaveVideoCamsOff():
    setSaveVideoCams('0')


def setSaveVideoCamsOn():
    setSaveVideoCams('1')


def setAutoTermo(value):
    global pathConfigDB
    global SQL_AUTOTERMO_UPDATE
    global sendFile

    sql = SQL_AUTOTERMO_UPDATE
    try:
        redisSet('configautoTermo', value)
        sqlExec = sql.replace('valor', value)
        DB = sqlite3.connect(pathConfigDB)
        cur = DB.cursor()
        cur.execute(sqlExec)
        DB.commit()
        cur.close()
        DB.close()
        toFile(sendFile, "AutoTermo actualizado a " + value)
        return True
    except Exception as e:
        toLogFile('Error setAutoTermo: ' + str(e))
        return False


def setAutoTermoOff():
    setAutoTermo('0')


def setAutoTermoOn():
    setAutoTermo('1')


initGlobalVars()

