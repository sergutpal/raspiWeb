#!/usr/bin/python

import globalVars
import time

globalVars.getValues(globalVars.pathEfergyDB, 'ENERGIA', 'efergy',
                     'historicoefergy', 'energia', 'W', globalVars.sendFile)
txtOut = "PVNow: " + str(globalVars.redisGet(globalVars.redisPVNow))
txtOut = txtOut + "W. PVSumToday: " + str(globalVars.redisGet(globalVars.redisPVSumToday)) + "KW"
time.sleep(0.5)
globalVars.toFile(globalVars.sendFile, txtOut)