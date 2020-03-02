# -*- coding: utf-8 -*-

import time
from _thread import start_new_thread
import sqlite3
import django
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import globalVars
from musica import musicaPlay
from musicaoff import musicaOff
from kodi import kodiPlay
from foto import photoRequest
from temperatura import sendLastTemperatureTelegram
from abreparking import parkingRequest
from flush import flushAll
from wakeonlan import wakeonlanRequest
from ip import get_ip_public
from MQTTSend import pubMQTTMsg
import MQTTServer


def getValueDB(pathDB, tableName, columnName, unity):
    try:
        DB = sqlite3.connect(pathDB.replace('X', '2DHT22'))
        cur = DB.cursor()
        values = globalVars.getActualValue(
            cur, tableName, columnName, unity, False)

    except Exception as e:
        globalVars.toLogFile('Error getValueDB: ' + str(e))
        values = {'value': '', 'time': ''}
    finally:
        cur.close()
        DB.close()
    return values


def inicioMin(notifMsg):
    alarma = globalVars.isAlarmActive()
    auto = globalVars.isAlarmAuto()
    parking = globalVars.isParkingOpen()
    djangovers = django.VERSION

    values = {'notifMsg': notifMsg, 'alarma': alarma, 'auto': auto,
              'parking': parking, 'djangovers': djangovers}
    return values


@login_required
def inicio(request, notifMsg=''):
    values = inicioMin(notifMsg)
    values.update({'seeAll': False})
    msg = 'Peticion Web CubieSrv: ' + notifMsg
    globalVars.toLogFile(msg)
    if notifMsg:
        globalVars.toFile(globalVars.sendFile, msg)
    return render(request, 'inicio.html', values)



@login_required
def inicioFull(request, notifMsg=''):
    values = inicioMin(notifMsg)
    values.update({'seeAll': True})

    energia = getValueDB(globalVars.pathEfergyDB, 'efergy', 'energia', ' W')
    temperatura_calle = getValueDB(globalVars.pathTemperatureDB.replace(
        'X', '2DHT22'), 'temperatura', 'temperatura', ' grados')
    temperatura_salon = getValueDB(globalVars.pathTemperatureDB.replace(
        'X', '1'), 'temperatura', 'temperatura', ' grados')
    temperatura_dormitorio = getValueDB(globalVars.pathTemperatureDB.replace(
        'X', '3'), 'temperatura', 'temperatura', ' grados')
    pathPhotos = getPathPhoto()
    ip = get_ip_public()

    valuesFull = {'energiaValue': energia['value'],
                  'energiaTime': energia['time'],
                  'ip': ip,
                  'temperatura_calleValue': temperatura_calle['value'],
                  'temperatura_calleTime': temperatura_calle['time'],
                  'temperatura_salonValue': temperatura_salon['value'],
                  'temperatura_salonTime': temperatura_salon['time'],
                  'temperatura_dormitorioValue': temperatura_dormitorio['value'],
                  'temperatura_dormitorioTime': temperatura_dormitorio['time']}
    values.update(valuesFull)
    values.update(pathPhotos)
    return render(request, 'inicio.html', values)


def checkURLOnOff(active, msgNotif='', msgFemale=False):
    if active.lower() == 'on':
        set = True
        active = True
        status = msgNotif + ' activado correctamente'
    elif active.lower() == 'off':
        set = True
        active = False
        status = msgNotif + ' desactivado correctamente'
    else:
        set = False
        active = None
        status = ''
    if (msgFemale):
        status = status.replace('activado', 'activada')
    return {'active': active, 'status': status, 'set': set}


def setValueOnOff(active, topic, msgNotif, msgFemale):
    try:
        values = checkURLOnOff(active, msgNotif, msgFemale)
        if values['set']:
            if values['active']:
               payload = MQTTServer.payloadAlarmaON
            else:
               payload = MQTTServer.payloadAlarmaOFF
            globalVars.toLogFile('setValueOnOff antes de publicar ')
            pubMQTTMsg(topic, payload)
        return values
    except Exception as e:
        globalVars.toLogFile('Error setValueOnOff: ' + str(e))


@login_required
def auto(request, active):
    values = setValueOnOff(active, MQTTServer.topicAlarmaAuto, 'Modo auto', False)
    return inicio(request, values['status'])


@login_required
def alarma(request, active):
    values = setValueOnOff(active, MQTTServer.topicAlarma, 'Alarma', True)
    return inicio(request, values['status'])


@login_required
def musica(request, active=''):
    values = checkURLOnOff(active, None)
    if values['active']:
        musicaPlay(False, False)
        msgNotif = 'Solicitud encender musica enviada'
    else:
        musicaOff(False)
        msgNotif = 'Solicitud apagar musica enviada'
    return inicio(request, msgNotif)


@login_required
def musica1OR4(request, piNumber='0'):
    if (piNumber == '1') or (piNumber == '4'):
        globalVars.redisRequestSet(
            globalVars.redisMP3StreamingRequest.replace('X', piNumber))
    return inicio(request, 'Solicitud musica en ' + piNumber + ' enviada')


@login_required
def kodi(request, piNumber=0):
    if piNumber > 0:
        kodiPlay(piNumber, False)
    return inicio(request, 'Solicitud Kodi' + str(piNumber) + ' enviada')


def getPathPhoto():
    pathMedia = '/media/RaspiX.jpg'
    return {'raspi1': pathMedia.replace('X', '1'),
            'raspi2': pathMedia.replace('X', '2'),
            'raspi3': pathMedia.replace('X', '3'),
            'raspi4': pathMedia.replace('X', '4')}


@login_required
def foto(request, piNumber='0'):
    photoRequest(int(piNumber))
    time.sleep(5)
    # pathPhotos = getPathPhoto()
    return inicio(request, 'Solicitud foto ' + piNumber + ' enviada')


@login_required
def temperatura(request, piNumber='0'):
    sendLastTemperatureTelegram()
    time.sleep(5)
    return inicio(request, 'Solicitud temperatura ' + piNumber + ' enviada')


@login_required
def parking(request, waitSeconds='-1'):
    waitSeconds = int(waitSeconds)
    if waitSeconds >= 0:  # La ejecucion es forzada! No hay que pasar por la
                          # pantalla de confirmacion!! No es aconsejable este
                          # modo y es mejor deshabilitarlo
        waitSeconds = str(waitSeconds)
        parkingRequest(waitSeconds)
        return inicio(request, 'Abriendo parking en ' +
                      waitSeconds + ' segundos')

    CONFIRM_OPEN = 'confirmOpen'
    WAIT_SECONDS = 'waitSeconds'
    if CONFIRM_OPEN in request.POST and request.POST[CONFIRM_OPEN]:
        confirm = request.POST[CONFIRM_OPEN]
        if confirm == CONFIRM_OPEN:
            if WAIT_SECONDS in request.POST and request.POST[WAIT_SECONDS]:
                try:
                    waitSeconds = request.POST[WAIT_SECONDS]
                except Exception:
                    waitSeconds = '0'
            else:
                waitSeconds = '0'
            parkingRequest(waitSeconds)
            return inicio(request, 'Abriendo parking en ' + waitSeconds +
                          ' segundos')
    return render(request, 'parking.html', {'confirm': False})


@login_required
def wakeonlan(request):
    wakeonlanRequest(False)
    return inicio(request, 'Solicitud wakeonlan enviada')


@login_required
def reboot(request, piNumber='-1'):
    if piNumber != '-1':
        start_new_thread(globalVars.rebootRequest, (False, piNumber))
        # if piNumber == '0':
        #     allPi = True
        # else:
        #     allPi = False

        # return render(request, 'reboot.html', {'confirm': True, 'allPi':
        # allPi, 'piNumber':piNumber})
        return inicio(request, 'Solicitud reboot ' + piNumber + ' enviada')
    CONFIRM = 'confirm'
    PI_NUMBER = 'piNumber'
    if CONFIRM in request.POST and request.POST[CONFIRM]:
        confirm = request.POST[CONFIRM]
        if confirm == CONFIRM:
            if PI_NUMBER in request.POST and request.POST[PI_NUMBER]:
                try:
                    piNumber = request.POST[PI_NUMBER]
                except Exception:
                    piNumber = '0'
            else:
                piNumber = '0'
            start_new_thread(
                globalVars.rebootRequest, (False, piNumber))
            # if piNumber == '0':
            #     allPi = True
            # else:
            #     allPi = False
            return inicio(request, 'Solicitud reboot ' + piNumber + ' enviada')
    return render(request, 'reboot.html',
                  {'confirm': False, 'allPi': False, 'piNumber': '0'})


@login_required
def watchdog(request, piNumber='0'):
    globalVars.watchdogRequest(False, piNumber)
    # if piNumber == '0':
    #     allPi = True
    # else:
    #     allPi = False
    return inicio(request, 'Solicitud watchdog ' + piNumber + ' enviada')


@login_required
def transmissionON(request):
    globalVars.supervisor('transmission', True)
    return inicio(request, 'Solicitud Transmission ON enviada')


@login_required
def transmissionOFF(request):
    globalVars.supervisor('transmission', False)
    return inicio(request, 'Solicitud Transmission OFF enviada')


@login_required
def flush(request):
    flushAll()
    return inicio(request, 'Solicitud Flush enviada')


@login_required
def firewallON(request):
    globalVars.firewall('on')
    return inicio(request, 'Solicitud Firewall ON enviada')


@login_required
def firewallOFF(request):
    globalVars.firewall('off')
    return inicio(request, 'Solicitud Firewall OFF enviada')
