#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este modulo elimina todas los valores de redis para que se vuelva a inicializar todo (especialmente 
# los parametros del config)

import globalVars
import redis


def flushRedis():
    try:
        redisSrv = globalVars.redisSrv
        redisSrv.flushall()
        globalVars.toFile(globalVars.sendFile, "Redis flushall")
        return True
    except Exception as e:
        globalVars.toLogFile('Error flushRedis: ' + str(e))
        return False


def flushAll():
    flushRedis()


if __name__ == "__main__":
    flushAll()
