#!/usr/bin/python

import globalVars

raspiId = __file__.replace('.py', '')[-1:]
globalVars.redisRequestSet(
    globalVars.redisMP3StreamingRequest.replace('X', raspiId))
globalVars.toFile(globalVars.sendFile, "M" + raspiId + " PLAYing")
