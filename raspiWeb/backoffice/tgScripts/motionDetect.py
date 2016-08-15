#!/usr/bin/python
import globalVars

MAX_SECONDS_ALERT_MOTION = 600


def motionAlert():
    global MAX_SECONDS_ALERT_MOTION

    if not globalVars.isAlarmActive():
        return None
    motionFirstMinuteIgnore = globalVars.redisMotionFirstMinuteIgnore.replace(
        'X', globalVars.raspiId)
    if globalVars.redisGet(motionFirstMinuteIgnore):
        return None
    globalVars.toLogFile('MotionAlert real!')
    motionRedis = globalVars.redisAlarmMotionRequest.replace(
        'X', globalVars.raspiId)
    if globalVars.redisGet(motionRedis):
        return None     # ya se ha producido un aviso de alerta de motion.
    strAlert = 'ALERTA MOTION EN ' + globalVars.raspiName + '!!!'
    globalVars.redisSet(motionRedis, strAlert, MAX_SECONDS_ALERT_MOTION)
    globalVars.toLogFile(strAlert)
    return True

if __name__ == "__main__":
    motionAlert()
