#!/usr/bin/python

import globalVars
import datetime
import time
import os
import dropbox

PINGFILE = 'ping.txt'


class DropBoxTransfer:
    def __init__(self):
        # sergutpalrpi@gmail.com
        access_token = '_v-BqRmJ1ZAAAAAAAAAALI8Oy4QfZyllBVyDU7hAU6F8-QOiTEevNqq1-GZ6OLOi'

        self.access_token = access_token

    def uploadFile(self, deleteOrigin=True, fileFromPath=None, fileFromName=None, fileTo=None):
        try:
            fechaHora = time.gmtime()
            fechaAnyo = time.strftime('%Y', fechaHora)
            fechaMes = time.strftime('%m', fechaHora)
            fechaDia = time.strftime('%d', fechaHora)
            if not fileFromName:
                fileFromName = datetime.datetime.now().strftime("%H%M%S.%f")
            if not fileTo:
                fileTo = '/cubieSrv/' + fechaAnyo + '/' + fechaMes + '/'+fechaDia + '/'
                fileTo = fileTo + fileFromName

            if os.path.exists(fileFromPath):
                dbx = dropbox.Dropbox(self.access_token)
                f = open(fileFromPath)
                f = f.read()
                globalVars.toLogFile('DropBox: ' + fileFromPath)
                dbx.files_upload(f, fileTo, mode=dropbox.files.WriteMode('overwrite', None), autorename=False, mute=True)
                if deleteOrigin:
                    os.remove(fileFromPath)
            else:
                raise Exception(fileFromPath + ' no exite!')
                return False
            return True
        except Exception as e:
            globalVars.toLogFile('Error uploadFile: ' + str(e))
            return False

    def uploadFolder(self, path=None):
        if not path:
            path = globalVars.pathDropBox
        try:
            files = (file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)))
            for file in files:
                self.uploadFile(True, path + file, file)
            return True
        except Exception as e:
            globalVars.toLogFile('Error uploadFolder: ' + str(e))
        return False



def dropBoxUpdatePing():
    global PINGFILE

    try:
        fechaHora = time.gmtime()
        fechaHora = time.strftime('%d/%m/%Y %H:%M:%S', fechaHora)

        dbx = DropBoxTransfer()

        fileFromName = PINGFILE
        fileFrom = globalVars.pathTmp + fileFromName
        globalVars.toFile(fileFrom, fechaHora, True, 'w')
        dbx.uploadFile(False, fileFrom, fileFromName, '/' + fileFromName)

        return True
    except Exception as e:
        globalVars.toLogFile('Error dropBoxUpdatePing: ' + str(e))
    return False


def dropBoxSync():
    try:
        dbx = DropBoxTransfer()
        dbx.uploadFolder()

        return True
    except Exception as e:
        globalVars.toLogFile('Error dropBoxSync: ' + str(e))
    return False


if __name__ == "__main__":
    dropBoxUpdatePing()
