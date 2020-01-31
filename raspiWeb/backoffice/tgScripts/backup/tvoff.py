#!/usr/bin/python

import globalVars

for i in range(1, globalVars.numRaspis + 1):
    globalVars.redisRequestSet(
        globalVars.redisTVOffRequest.replace('X', str(i)))
    globalVars.toFile(globalVars.sendFile, 'Solicitud apagar TV enviada')
