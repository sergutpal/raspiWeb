#!/usr/bin/python
import time
import globalVars
import picamera
import shutil

camera = None
DELAY_FROM_PHOTOS = 1
pathTmp = '/tmp/'
extensionPhoto = '.png'


def RpiCamRaspiMJPEG(start):
    try:
        if start:
            if not globalVars.RpiCamStarted:
                cmd = 'ru 1'
            else:
                cmd = ''
        else:
            if globalVars.RpiCamStarted:
                cmd = 'ru 0'
            else:
                cmd = ''
        pathFIFO = globalVars.pathRpiCamFIFO
        globalVars.toFile(pathFIFO, cmd, False)
        globalVars.RpiCamStarted = start
        if start:
            # Esperamos 2 segundos para que no se pierda ninguna comanda
            time.sleep(2)
        return globalVars.RpiCamStarted
    except Exception as e:
        globalVars.toLogFile('Error RpiCam ' + str(start) + ': ' + str(e))
        return globalVars.RpiCamStarted


def RpiCamPhoto(closeRpiCam, sendTelegram=False):
    global pathTmp
    try:
        if not globalVars.RpiCamStarted:
            RpiCamRaspiMJPEG(True)
        globalVars.toFile(globalVars.pathRpiCamFIFO, 'im', False)
        time.sleep(1)
        if closeRpiCam:
            RpiCamRaspiMJPEG(False)
        tmpFile = pathTmp + 'raspi' + globalVars.raspiId + \
            '_' + time.strftime('%d%m%y_%H%M%S') + '.jpg'
        fileName = 'raspi' + globalVars.raspiId + '.jpg'
        fileTo = pathTmp + fileName
        shutil.copyfile(globalVars.pathRpiCamJPG, tmpFile)
        if sendTelegram:
            shutil.copyfile(tmpFile, globalVars.pathTmpTelegram + fileName)
        shutil.move(tmpFile, globalVars.pathDropBoxFrom)
        return fileTo
    except Exception as e:
        globalVars.toLogFile('Error capturando fotografia (RpiCam): ' + str(e))
        return ''


def cameraPhoto(closeRpiCam, sendTelegram=False):
    try:
        return RpiCamPhoto(closeRpiCam, sendTelegram)
    except Exception as e:
        globalVars.toLogFile('Error capturando fotografia (RpiCam): ' + str(e))
    return ''


def cameraAlarm():
    global camara
    global path

    try:
        for i in range(0, 60):
            cameraPhoto(False, False)
            time.sleep(DELAY_FROM_PHOTOS)
        RpiCamRaspiMJPEG(False)
    except Exception as e:
        globalVars.toLogFile('Error cameraAlarm (picamara): ' + str(e))
    return


def initCamera():
    global camera
    global path

    try:
        camera = picamera.PiCamera()
        camera.brightness = 50  # [0..100]
        camera.contrast = 0  # [0..100]
        camera.saturation = 0  # [0..100]
        camera.ISO = 0  # [0..100]
        camera.hflip = True
        camera.vflip = True
        camera.resolution = (640, 480)
    except Exception as e:
        globalVars.toLogFile('Error inicializando piCamera: ' + str(e))
    return


if __name__ == "__main__":
    cameraPhoto(True)
