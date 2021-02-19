# -*- coding: utf-8 -*-
import time
from MQTTSend import pubMQTTMsg
import MQTTServer
import globalVars

SEGUNDOS_APAGADO_BOMBA_AUTO = '900'  # 15 min = 900 secs
EMERGENCIA_AGUA = '-9999'
NOAUTO = '-1111'

def isEmergencia():
    emergencia = globalVars.redisGet(globalVars.redisBombaAguaAutoOff, False)
    if (emergencia ==EMERGENCIA_AGUA):
        return True
    else:
        return False


def isBombaAuto():
    noAuto = globalVars.redisGet(globalVars.redisBombaAguaNoAuto, False)
    if (noAuto ==NOAUTO):
        return False
    else:
        return True


def enciendeBombaAgua():
    # No hace falta llamar a bombaAguaEncendida pq lo hará la captura del mensaje MQTT en MQTTSub.getMQTTBombaAgua
    globalVars.redisDelete(globalVars.redisBombaAguaNoAuto)
    pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaON)


def enciendeBombaAguaNoAuto():
    # No hace falta llamar a bombaAguaEncendida pq lo hará la captura del mensaje MQTT en MQTTSub.getMQTTBombaAgua
    globalVars.redisSet(globalVars.redisBombaAguaNoAuto, NOAUTO)
    pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaON)


def apagaBombaAgua():
    if (not isEmergencia()):
        pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaOFF)
        globalVars.redisDelete(globalVars.redisBombaAguaNoAuto)


def bombaAguaEncendida():
    # Este método se llama después de que se haya activado el switch de Enchufe3 por MQTT/Homeassistant/etc, para arrancar la bomba de agua (cerrando también la electroválvula)
    if (isBombaAuto() and not isEmergencia()):
        globalVars.redisSet(globalVars.redisBombaAguaAutoOff, SEGUNDOS_APAGADO_BOMBA_AUTO)
        globalVars.toFile(globalVars.sendFile, "Bomba agua encendida modo auto. En unos minutos se apagará")
    else:
        if (not isBombaAuto() and not isEmergencia()):
            globalVars.toFile(globalVars.sendFile, "Bomba agua encendida. El apagado NO está en modo auto!")
        else:
            globalVars.toFile(globalVars.sendFile, "Bomba agua encendida por modo emergencia!!")


def bombaAguaApagada():
    # Este método se llama después de que se haya desactivado el switch de Enchufe3 por MQTT/Homeassistant/etc, para apagar la bomba de agua (abriendo también la electroválvula)
    if (isEmergencia()):
        # Si se ha activado la emergencia del agua, no podemos permitir que la electroválvula se apague permitiendo la entrada de agua!
        # En este caso, debemos volver a encender la bomba y lo más rápido posible, pero esperamos un par de segundos para que el relé conmute bien!!
        time.sleep(2)
        pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaON)
    else:
        globalVars.toFile(globalVars.sendFile, "Bomba agua apagada")
        globalVars.redisDelete(globalVars.redisBombaAguaAutoOff)
    globalVars.redisDelete(globalVars.redisBombaAguaNoAuto)


def apagaBombaAuto(secsApagado=SEGUNDOS_APAGADO_BOMBA_AUTO):
    # Una vez encendemos la bomba p. ej. para la ducha, queremos despreocuparnos de tener que apagarla automáticamente. La idea es que después de X minutos (20?) la raspi 
    # se encargue del apagado automático

    # Por si acaso, antes de apagar la bomba, revisamos que no estemos en el modo Emergencia
    emergencia = globalVars.redisGet(globalVars.redisBombaAguaAutoOff, False)
    if (emergencia !=EMERGENCIA_AGUA):
        globalVars.redisDelete(globalVars.redisBombaAguaAutoOff)
        globalVars.redisDelete(globalVars.redisBombaAguaNoAuto)
        if secsApagado > 0:
            time.sleep(secsApagado)
        pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaOFF)


# Este es el método que debe llamar el sensor Aqara inmersion agua que tenemos dentro del depósito de agua si se activa
def alarmaAgua(strAlert):
    # Si Aqara inmersion detecta agua (una emergencia), queremos que corte el suministro de agua (activando el enchufe3 de la bomba de agua que cerrará
    # la electroválvula de la entrada de la acometida) y que nos avise rápidamente por todos los medios para evitar cualquier tipo de colapso.
    globalVars.redisSet(globalVars.redisBombaAguaAutoOff, EMERGENCIA_AGUA)
    enciendeBombaAgua()
    globalVars.fireAlarm(strAlert)


if __name__ == "__main__":
    enciendeBombaAgua()