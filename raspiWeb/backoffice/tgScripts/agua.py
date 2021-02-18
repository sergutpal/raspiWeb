# -*- coding: utf-8 -*-
import time
from MQTTSend import pubMQTTMsg
import MQTTServer
import globalVars

SEGUNDOS_APAGADO_BOMBA_AUTO = '900'  # 15 min = 900 secs
EMERGENCIA_AGUA = '-9999'

def isEmergencia():
    emergencia = globalVars.redisGet(globalVars.redisBombaAguaAutoOffRequest, False)
    if (emergencia ==EMERGENCIA_AGUA):
        return True
    else:
        return False


def enciendeBombaAgua():
    pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaON)


def apagaBombaAgua():
    if (not isEmergencia()):
        pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaOFF)


def bombaAguaEncendida(apagaAuto=True):
    # Este método se llama después de que se haya activado el switch de Enchufe3 por MQTT/Homeassistant/etc, para arrancar la bomba de agua (cerrando también la electroválvula)
    globalVars.toFile(globalVars.sendFile, "Bomba agua encendida")
    if (apagaAuto and not isEmergencia()):
        globalVars.toFile(globalVars.sendFile, "Alucino2...")
        globalVars.redisRequestSet(globalVars.redisBombaAguaAutoOffRequest, SEGUNDOS_APAGADO_BOMBA_AUTO)


def bombaAguaApagada():
    # Este método se llama después de que se haya desactivado el switch de Enchufe3 por MQTT/Homeassistant/etc, para apagar la bomba de agua (abriendo también la electroválvula)
    if (isEmergencia()):
        # Si se ha activado la emergencia del agua, no podemos permitir que la electroválvula se apague permitiendo la entrada de agua!
        # En este caso, debemos volver a encender la bomba y lo más rápido posible, pero esperamos un par de segundos para que el relé conmute bien!!
        time.sleep(2)
        pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaON)
    else:
        globalVars.redisDelete(globalVars.redisBombaAguaAutoOffRequest)
        globalVars.toFile(globalVars.sendFile, "Bomba agua apagada")


def apagaBombaAuto(secsApagado=SEGUNDOS_APAGADO_BOMBA_AUTO):
    # Una vez encendemos la bomba p. ej. para la ducha, queremos despreocuparnos de tener que apagarla automáticamente. La idea es que después de X minutos (20?) la raspi 
    # se encargue del apagado automático

    # Por si acaso, antes de apagar la bomba, revisamos que no estemos en el modo Emergencia
    emergencia = globalVars.redisGet(globalVars.redisBombaAguaAutoOffRequest, False)
    if (emergencia !=EMERGENCIA_AGUA):
        globalVars.toFile(globalVars.sendFile, "Alucino...")
        globalVars.redisDelete(globalVars.redisBombaAguaAutoOffRequest)
        if secsApagado > 0:
            time.sleep(secsApagado)
        pubMQTTMsg(MQTTServer.topicBombaAgua, MQTTServer.payloadAlarmaOFF)


# Este es el método que debe llamar el sensor Aqara inmersion agua que tenemos dentro del depósito de agua si se activa
def emergenciaAgua():
    # Si Aqara inmersion detecta agua (una emergencia), queremos que corte el suministro de agua (activando el enchufe3 de la bomba de agua que cerrará
    # la electroválvula de la entrada de la acometida) y que nos avise rápidamente por todos los medios para evitar cualquier tipo de colapso.
    globalVars.redisRequestSet(globalVars.redisBombaAguaAutoOffRequest, EMERGENCIA_AGUA)
    enciendeBombaAgua()
    strAlert = "EMERGENCIA DE AGUA!!!!!!!! REVISA QUE LA ELECTROVALVULA ESTÉ ENCENDIDA. POR SI ACASO, ENVIA EL COMANDO agua!!!"
    globalVars.toFile(globalVars.sendFile, strAlert)
    globalVars.redisSet(globalVars.redisPhoneAlarmRequest, strAlert)
    for i in range(0, globalVars.numRaspis + 1):
        globalVars.redisRequestSet(globalVars.redisAlarmRequest.replace('X',str(i)))


if __name__ == "__main__":
    enciendeBombaAgua()