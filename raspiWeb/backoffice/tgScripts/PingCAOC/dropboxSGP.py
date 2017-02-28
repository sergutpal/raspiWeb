#!/usr/bin/python

import globalVars
import datetime
import time
import os
import dropbox
import telegramSGP


class DropBoxTransfer:
    def __init__(self):
        # sergutpalrpi@gmail.com
        access_token = '_v-BqRmJ1ZAAAAAAAAAALI8Oy4QfZyllBVyDU7hAU6F8-QOiTEevNqq1-GZ6OLOi'

        self.access_token = access_token

    def uploadFile(self, deleteOrigin=True, fileFromPath=None, fileFromName=None, fileToPath=None, fileToName=None):
        try:
            fechaHora = time.gmtime()
            fechaAnyo = time.strftime('%Y', fechaHora)
            fechaMes = time.strftime('%m', fechaHora)
            fechaDia = time.strftime('%d', fechaHora)
            if not fileFromName:
                fileFromName = datetime.datetime.now().strftime("%H%M%S.%f")
            if not fileToPath:
                fileToPath = globalVars.pathDropBoxTo + fechaAnyo + '/' + fechaMes + '/'+fechaDia + '/'
            if not fileToName:
                fileToName = fileFromName

            if os.path.exists(fileFromPath):
                dbx = dropbox.Dropbox(self.access_token)
                f = open(fileFromPath)
                f = f.read()
                globalVars.toLogFile('DropBox upload: ' + fileFromPath)
                dbx.files_upload(f, fileToPath +fileToName, mode=dropbox.files.WriteMode('overwrite', None), autorename=False, mute=True)
                if deleteOrigin:
                    os.remove(fileFromPath)
            else:
                raise Exception(fileFromPath + ' no exite!')
                return False
            return True
        except Exception as e:
            globalVars.toLogFile('Error uploadFile: ' + str(e))
            return False

    def uploadFolder(self, pathFrom=None, pathTo=None):
        if not pathFrom:
            pathFrom = globalVars.pathDropBoxFrom
        try:
            files = (file for file in os.listdir(pathFrom) if os.path.isfile(os.path.join(pathFrom, file)))
            for file in files:
                self.uploadFile(True, pathFrom + file, file, pathTo, file)
            return True
        except Exception as e:
            globalVars.toLogFile('Error uploadFolder: ' + str(e))
        return False

    def downloadFile(self, pathFrom, pathTo=None):
        try:
            dbx = dropbox.Dropbox(self.access_token)
            globalVars.toLogFile('DropBox download: ' + pathFrom)
            metadata, res = dbx.files_download(pathFrom)
            content = res.content
            if pathTo:
                with open(pathTo, "w") as f:
                    f.write(content.decode('utf-8'))
                    f.close()
            return content
        except Exception as e:
            globalVars.toLogFile('Error downloadFile: ' + str(e))
        return False


def dropBoxReadPing():
    try:
        dbx = DropBoxTransfer()
        content = dbx.downloadFile(globalVars.pathDropBoxToPing + globalVars.PINGFILE, None)
        content = content.decode('utf-8')
        content = content.replace('\n', '')
        globalVars.toLogFile('Ping: ' + content)
        return content
    except Exception as e:
        globalVars.toLogFile('Error dropBoxReadPing: ' + str(e))
    return None


def checkDropboxPingIsExpired():
    try:
        pingTimeStr = dropBoxReadPing()
        if not pingTimeStr:
            return True
        pingTime = datetime.datetime.strptime(pingTimeStr, '%d/%m/%Y %H:%M:%S')
        now = datetime.datetime.now()
        secondsDiff = (now - pingTime).total_seconds()
        if secondsDiff > 2400:   # 40 minutos            
            return True
        return False
    except Exception as e:
        globalVars.toLogFile('Error checkDropboxPingIsExpired: ' + str(e))
    return True


if __name__ == "__main__":
    checkDropboxPingIsExpired()
