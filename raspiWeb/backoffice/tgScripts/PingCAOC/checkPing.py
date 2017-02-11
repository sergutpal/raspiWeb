#!/usr/bin/python

import globalVars
import dropboxSGP
import datetime
import time
import os
import telegramSGP


def checkPing():
    try:
        ping = dropboxSGP.checkDropboxPingIsExpired()
        if (ping):
            msg = 'Ping Expirado! CubieSrv NO disponible'
            telegramSGP.sendTelegramBot(msg)
            print(msg)
        return True
    except Exception as e:
        globalVars.toLogFile('Error checkPing: ' + str(e))
    return False



if __name__ == "__main__":
    checkPing()
