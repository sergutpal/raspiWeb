#!/usr/bin/python
import time
import globalVars
import picamera
import shutil

camera = None
DELAY_FROM_PHOTOS = 1
pathTmp = '/tmp/'
extensionPhoto = '.png'


def stopCamera():
    try:
        time.sleep(DELAY_FROM_PHOTOS)
        cmd = 'ru 0'
        pathFIFO = globalVars.pathRpiCamFIFO
        globalVars.toFile(pathFIFO, cmd, False, 'w')
        globalVars.RpiCamStarted = False
        return True
    except Exception as e:
        globalVars.toLogFile('Error stopCamera: ' + str(e))
        return False


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
        globalVars.toFile(pathFIFO, cmd, False, 'w')
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
        globalVars.toFile(globalVars.pathRpiCamFIFO, 'im', False, 'w')
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


def RpiCamVideo(closeRpiCam, timeSecs):
    global pathTmp
    try:
        if not globalVars.RpiCamStarted:
            RpiCamRaspiMJPEG(True)
        globalVars.toFile(globalVars.pathRpiCamFIFO, 'ca 1 ' + str(timeSecs), False, 'w')
        fileName = 'Raspi' + globalVars.raspiId + \
            '_' + time.strftime('%Y%m%d_%H%M%S') + '.mp4'
        pathFile = globalVars.pathRpiCamMedia + fileName
        time.sleep(timeSecs +5) # RpiCam tarda unos segundos en crear el mp4. Hay que darle margen antes de intentar copiar el fichero al destino final
        if closeRpiCam:
            RpiCamRaspiMJPEG(False)
        shutil.move(pathFile, globalVars.pathDropBoxFromVideo + fileName)
        return pathFile
    except Exception as e:
        globalVars.toLogFile('Error capturando video (RpiCam): ' + str(e))
        return ''


def cameraPhoto(closeRpiCam, sendTelegram=False):
    try:
        return RpiCamPhoto(closeRpiCam, sendTelegram)
    except Exception as e:
        globalVars.toLogFile('Error capturando fotografia (RpiCam): ' + str(e))
    return ''


def cameraVideo(closeRpiCam, timeSecs):
    try:
        return RpiCamVideo(closeRpiCam, timeSecs)
    except Exception as e:
        globalVars.toLogFile('Error capturando video (RpiCam): ' + str(e))
    return ''


def cameraStart(sendTelegram=True):
    try:
        if not globalVars.RpiCamStarted:
            RpiCamRaspiMJPEG(True)
        return True
    except Exception as e:
        globalVars.toLogFile('Error cameraStart: ' + str(e))
        return False


def cameraAlarm():
    global camara
    global path

    try:
        for i in range(0, 60):
            cameraPhoto(False, False)
            time.sleep(DELAY_FROM_PHOTOS)
        stopCamera()
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
