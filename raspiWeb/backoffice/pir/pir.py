#!/usr/bin/python
import camara
import insertTemperatura
import globalVars
import RPi.GPIO as GPIO
import time
import thread
import subprocess
import sqlite3

CHECK_SECONDS = 0.5     # Los sensores se comprueban cada CHECK_SECONDS
PARKING_PULSE = 1.5     # Cuanto tiempo el rele que manda el pulsador del
                        # parking debe estar apretado para abrir el motor
                        # del parking
WAIT_SECONDS_ALARM = 600
waitingAlarm = 0
parkingPIN = 33  # GPIO13
buzzerPIN = 40  # GPIO21
pirPIN = 11  # GPIO17
doorPIN = 37  # GPIO26 ; Switch rele para detectar la puerta abierta
buzzerTimes = 100
parkingCheckTimes = 0
parkingLastValue = -1
parkingLastValueDB = -1


def initGPIO():
    global buzzerPIN
    global pirPIN
    global doorPIN

    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(buzzerPIN, GPIO.OUT)
        GPIO.output(buzzerPIN, 0)
        GPIO.setup(pirPIN, GPIO.IN)
        GPIO.setup(doorPIN, GPIO.IN)
        return 1
    except Exception as e:
        globalVars.toLogFile('Error inicializando GPIO: ' + str(e))
        return 0


def buzzer(freq):
    global buzzerPIN
    global pirPIN
    global buzzerTimes

    print 'Buzzer: antes de comprobar el config'
    if globalVars.getConfigField('alarmBuzzerActive') =='0':
        # En la BD se ha indicado que no debe sonar el buzzer
        return None
    print 'Buzzer: despues de comprobar el config: ' + globalVars.getConfigField('alarmBuzzerActive')

    for x in range(0, buzzerTimes):
        # Si la alarma no esta activa, entonces no tocamos el buzzer. Esto
        # sirve para parar el buzzer si apagamos la alarma
        if (not globalVars.isAlarmActive()):
            return None
        GPIO.output(buzzerPIN, 1)
        time.sleep(freq)
        GPIO.output(buzzerPIN, 0)
        time.sleep(freq)
    return None


def playAlarmaKodi(pathAlarmaMP3):
    try:
        mp3Cmd = '/usr/bin/kodi ' + pathAlarmaMP3
        # volUPCmd = 'echo "volup" | cec-client -s'
        subprocess.Popen(mp3Cmd, shell=True)
        # for x in range(0, 20):
        #  try:
        #    process = subprocess.Popen(volUPCmd, shell = True)
        #    time.sleep(6)
        #  except Exception as ignore:
        #    globalVars.toLogFile('Error playAlarmaKodi: ' + str(e))
        return None
    except Exception as e:
        globalVars.toLogFile('Error playAlarmaKodi: ' + str(e))
    return None


def checkMP3StreamingRequest():
    if globalVars.redisRequestGet(
            globalVars.redisMP3StreamingRequest.replace('X',
                                                        globalVars.raspiId)):
        commandMP3 = '/usr/bin/mpg123 http://192.168.1.20:8000/mpd'
        try:
            subprocess.Popen(commandMP3, shell=True)
        except Exception as e:
            txt = str(e)
            globalVars.toLogFile('Error MP3 Streaming: ' + txt)
    return None


def openParking(waitSeconds=0):
    global parkingPIN
    global PARKING_PULSE

    try:
        if waitSeconds > 0:
            time.sleep(waitSeconds)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(parkingPIN, GPIO.OUT)
        GPIO.output(parkingPIN, True)
        time.sleep(PARKING_PULSE)
        GPIO.output(parkingPIN, False)
        globalVars.toLogFile('ABRIENDO PARKING!')
        return 1
    except Exception as e:
        print 'Error inicializando GPIO: ' + str(e) + '\n'
        return 0


def checkOpenParkingRequest():
    if (globalVars.raspiId != '2'):
        return None
    # Borramos la clave despues de leerla
    waitSeconds = globalVars.redisGet(globalVars.redisParkingRequest, True)
    if waitSeconds:
        waitSeconds = int(waitSeconds)
        thread.start_new_thread(openParking, (waitSeconds,))
    return True


def checkKodiRequest():
    if globalVars.redisRequestGet(globalVars.redisKodiRequest.replace('X',
                                  globalVars.raspiId)):
        command = '/usr/bin/kodi'
        try:
            subprocess.Popen(command, shell=True)
        except Exception as e:
            txt = str(e)
            globalVars.toLogFile('Error Kodi Start: ' + txt)
    return None


def checkRebootRequest():
    if globalVars.redisRequestGet(globalVars.redisRebootRequest.replace('X',
                                  globalVars.raspiId)):
        globalVars.rebootNow()
    return None


def checkWatchdogRequest():
    if globalVars.redisRequestGet(globalVars.redisWatchdogRequest.replace('X',
                                  globalVars.raspiId)):
        globalVars.watchdogNow()
    return None


def checkAlarmSetRequest():
    if globalVars.getConfigField('alarmMotionActive') =='0':
        # En la BD se ha indicado que no debemos activar el control por Motion
        return None

    if globalVars.redisRequestGet(globalVars.redisAlarmSetRequest.replace('X',
                                  globalVars.raspiId)):
        alarmOn = globalVars.isAlarmActive()
        # Debemos arrancar/parar la grabacion de la camara y motion
        camara.RpiCamRaspiMJPEG(alarmOn)
        globalVars.supervisor('motion', alarmOn)
        return True
    return None


def checkMotionAlarmRequest():
    if globalVars.getConfigField('alarmMotionActive') =='0':
        # En la BD se ha indicado que no debemos activar el control por Motion
        return False

    if globalVars.redisGet(globalVars.redisAlarmMotionRequest.replace('X',
                                  globalVars.raspiId)):
        # Tenemos una alerta de Motion! Debemos generar una alarma!
        return True
    return False


def checkPhotoRequest():
    if globalVars.redisRequestGet(globalVars.redisPhotoRequest.replace('X',
                                  globalVars.raspiId)):
        thread.start_new_thread(camara.cameraPhoto, (True,))
    return None


def checkTemperatureRequest():
    if globalVars.redisRequestGet(globalVars.redisTempetureInsertRequest.
                                  replace('X', globalVars.raspiId)):
        if (globalVars.raspiId == '2'):
            # Debemos llamar tambien a DHT22
            command = "/home/nfs/telegram/gpio/temperatura/ejecuta.sh"
            subprocess.Popen(command, shell=True)
        else:
            insertTemperatura.insertTemperaturePressure()
    return None


def checkTVOffRequest():
    if globalVars.getConfigField('alarmKodiActive') =='0':
        # En la BD se ha indicado que no debemos activar/parar Kodi
        return None

    # Solo Raspi1 y Raspi3 tienen HDMI 1.4
    if (globalVars.raspiId != '1') and (globalVars.raspiId != '3'):
        return None

    if globalVars.redisRequestGet(globalVars.redisTVOffRequest.
                                  replace('X', globalVars.raspiId)):
        commandTV = 'echo "standby 0" | cec-client -s '
        try:
            subprocess.Popen(commandTV, shell=True)
            time.sleep(5)
            commandHomeCinema = 'echo "standby 5" | cec-client -s '
            subprocess.Popen(commandHomeCinema, shell=True)
        except Exception as e:
            txt = str(e)
            globalVars.toLogFile('Error TVoff: ' + txt)
    return None


def checkTVOnRequest():
    # Solo Raspi1 y Raspi3 tienen HDMI 1.4
    if (globalVars.raspiId != '1') and (globalVars.raspiId != '3'):
        return None

    if globalVars.redisRequestGet(globalVars.redisTVOnRequest.replace('X',
                                  globalVars.raspiId)):
        thread.start_new_thread(playAlarmaKodi, (globalVars.pathTVOn, ))
    return None


def isPIRActive():
    global pirPIN

    if globalVars.getConfigField('alarmPIRActive') =='0':
        # En la BD se ha indicado que no debemos tener en cuenta el sensor PIR
        return False

    pirActive = GPIO.input(pirPIN)
    if (pirActive):
        return True
    else:
        return False


def isDoorOpen():
    global doorPIN

    if globalVars.getConfigField('alarmDoorActive') =='0':
        # En la BD se ha indicado que no debemos tener en cuenta el sensor de la puerta
        return False

    # Solo Raspi2 (parking) y Raspi4 (puerta principal) tienen doorOpen sensor
    if (globalVars.raspiId == '4') or (globalVars.raspiId == '2'):
        door = GPIO.input(doorPIN)
        if (door):
            return False    # Si el rele recibe un 1 entonces quiere decir que
                            # la puerta esta cerrada
        else:
            return True
    else:
        return False


def checkParkingChanged():
    global doorPIN
    global parkingCheckTimes
    global parkingLastValue
    global parkingLastValueDB

    if (globalVars.raspiId == '2'):
        # Si el rele recibe un 1 entonces quiere decir que la puerta esta
        # cerrada
        door = GPIO.input(doorPIN)
        if (door == 0):
            open = 1
        else:
            open = 0
        if parkingLastValue == -1:  # Es el valor por defecto de la primera
            # vez?
            # En caso afirmativo inicializamos al valor actual para no
            # actualizar el valor en BD ni mandar aviso
            parkingLastValue = open
        if parkingLastValueDB == -1:  # Es el valor por defecto de la primera
            # vez?
            # En caso afirmativo inicializamos al valor actual para no
            # actualizar el valor en BD ni mandar aviso
            parkingLastValueDB = open
        if (open == parkingLastValue) and (open == parkingLastValueDB):
            if parkingCheckTimes > 0:
                parkingCheckTimes = parkingCheckTimes - 1
            return False
        parkingLastValue = open
        if parkingCheckTimes == 0:  # No se ha enviado el aviso de parking
            # abierto: hay que enviarlo
            # Checkeamos cada 2 minutos que es lo que tarda el parking por
            # defecto en cerrarse automaticamente
            parkingCheckTimes = 120 / CHECK_SECONDS
            parkingLastValueDB = open
            setParking(open)
            return True
        else:
            parkingCheckTimes = parkingCheckTimes - 1
            return False
    else:
        return False


def setParking(open):
    SQL_PARKING_OPEN = 'INSERT INTO historicoParking(open, data) VALUES (' + \
                        str(open) + ', ' + globalVars.DATETIME_NOW + ' );'

    try:
        if open:
            globalVars.toFile(globalVars.sendFile, 'Parking Abierto!')
        else:
            globalVars.toFile(globalVars.sendFile, 'Parking cerrado')
        parkingDB = sqlite3.connect(globalVars.pathParkingDB)
        cur = parkingDB.cursor()
        cur.execute(SQL_PARKING_OPEN)
        parkingDB.commit()
        cur.close()
        parkingDB.close()
    except Exception as e:
        globalVars.toLogFile('Error parkingOpen: ' + str(e))
        return False
    return True

if __name__ == "__main__":
    CHECK_SECONDS = float(globalVars.getConfigField('checkSeconds'))
    buzzerTimes = int(globalVars.getConfigField('buzzerTimes'))
    ok = initGPIO()
    if (ok == 1):
        while (True):
            try:
                if (globalVars.isAlarmActive()):
                    pirActive = isPIRActive()
                    motionAlarm = checkMotionAlarmRequest()
                    doorOpen = isDoorOpen()
                    if ((pirActive or doorOpen or motionAlarm) and
                            waitingAlarm == 0):
                        waitingAlarm = WAIT_SECONDS_ALARM / CHECK_SECONDS
                        thread.start_new_thread(camara.cameraAlarm, ())
                        strAlert = globalVars.dateTime() + globalVars.raspiName
                        if pirActive:
                            strAlert = strAlert + ' PIR ACTIVO!!!\n'
                        elif motionAlarm:
                            strAlert = strAlert + ' ALARMA MOTION!!!\n'
                        else:  # DoorOpen
                            if globalVars.raspiId == '2':
                                strAlert = strAlert + \
                                    ' PARKING ABIERTO!!!\n'
                            else:  # Raspi4
                                strAlert = strAlert + \
                                    ' PUERTA PRINCIPAL ABIERTA!!!\n'
                        # Enviamos la senyal a CubieTruck para que llame por
                        # Asterisk a los moviles, envie los mails de alarma y
                        # reproduzca el mp3
                        globalVars.redisSet(
                            globalVars.redisPhoneAlarmRequest, strAlert)
                        for i in range(1, globalVars.numRaspis + 1):
                            globalVars.redisRequestSet(
                                globalVars.redisAlarmRequest.replace('X',
                                                                     str(i)))
                        globalVars.toFile(globalVars.alertFile, strAlert)
                checkParkingChanged()
                if globalVars.redisRequestGet(globalVars.redisAlarmRequest.
                                              replace('X',
                                                      globalVars.raspiId)):
                    # Alguna pi necesita que todos los buzzers piten:
                    # se esta produciendo una ALARMA!
                    # Comprobamos si ya estamos haciendo el aviso
                    previousCall = globalVars.redisGet(
                        globalVars.redisAlarmaYaAvisadaRaspi.
                        replace('X', globalVars.raspiId), False)
                    if previousCall is None:
                        globalVars.redisSet(globalVars.
                                            redisAlarmaYaAvisadaRaspi.
                                            replace('X', globalVars.raspiId),
                                            'Aviso ' +
                                            globalVars.raspiName, 600)
                        thread.start_new_thread(buzzer, (0.3,))
                        if globalVars.getConfigField('alarmMP3Active') =='1':
                            if (globalVars.raspiId == '1') or (
                                globalVars.raspiId == '3'):
                                thread.start_new_thread(
                                    playAlarmaKodi, (globalVars.pathAlarmaMP3, ))
                            elif globalVars.raspiId == '4':
                                thread.start_new_thread(
                                    globalVars.playMP3,
                                    (globalVars.pathAlarmaMP3, False))
                if waitingAlarm > 0:
                    waitingAlarm = waitingAlarm - 1
                globalVars.checkAlarmOffRequest()
                checkOpenParkingRequest()
                checkPhotoRequest()
                checkTemperatureRequest()
                checkTVOffRequest()
                checkTVOnRequest()
                checkMP3StreamingRequest()
                checkKodiRequest()
                checkRebootRequest()
                checkWatchdogRequest()
                checkAlarmSetRequest()
                time.sleep(CHECK_SECONDS)
            except Exception as e:
                txt = str(e)
                print 'Exception: ' + txt
                globalVars.toLogFile('Error Pir principal: ' + txt)
