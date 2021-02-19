# Prueba GIT 07022020
import paho.mqtt.client as mqtt
import json
from globalVars import toLogFile
from alarmaon import setAlarmOn
from alarmaoff import setAlarmOff
from auto import setAlarmAutoOn
from autooff import setAlarmAutoOff
from abreparking import parkingRequest
from wol import wakeonlanRequest
from woloff import wakeonlanOffRequest
import foto
import globalVars
import MQTTServer
import time
import agua


mqttc = None
disconnect_flag = False

def on_disconnect(client, userdata, rc):
    global disconnect_flag

    s = "MQTTSub DISCONNECT MQTT:  "  +str(rc) + "!!!"
    toLogFile(s)
    globalVars.toFile(globalVars.sendFile, s)
    disconnect_flag = True


def getMQTTParking(msg):
    globalVars.toFile(globalVars.sendFile, "Atención: petición MQTT abrir parking!!")


def checkMQTTPuertaParking(msg):
    try:
        js = json.loads(msg.payload)
        if js['contact']:
            # El sensor indica que la puerta del parking está cerrada. Debemos eliminar la señal en Redis para comprobar si superamos el máximo
            globalVars.redisDelete(globalVars.redisPuertaParkingAbierta)
        else:
            existeClave = globalVars.redisGet(globalVars.redisPuertaParkingAbierta, False)
            if (not existeClave):
                # Debemos insertar la señal con el timestamp para que en telegram.py controlemos si hemos superado el tiempo máximo para alertar
                fechahora = time.localtime()
                fechahora = time.strftime("%d/%m/%Y %H:%M:%S", fechahora)
                globalVars.redisSet(globalVars.redisPuertaParkingAbierta, fechahora)
    except Exception as e:
        toLogFile('Error checkMQTTPuertaParking: ' + str(e))


def getMQTTAlarma(msg):
    if (msg.payload ==MQTTServer.payloadAlarmaON):
        setAlarmOn('MQTT')
    if (msg.payload ==MQTTServer.payloadAlarmaOFF):
        setAlarmOff()


def getMQTTAlarmaAuto(msg):
#   toLogFile("Topic AlarmaAuto")
    if (msg.payload ==MQTTServer.payloadAlarmaON):
        setAlarmAutoOn('MQTT')
    if (msg.payload ==MQTTServer.payloadAlarmaOFF):
        setAlarmAutoOff('MQTT')


def getMQTTRadioParking(msg):
    if (msg.payload ==MQTTServer.payloadAlarmaON):
        globalVars.setRadioParkingOn()
    if (msg.payload ==MQTTServer.payloadAlarmaOFF):
        globalVars.setRadioParkingOff()


def getMQTTSaveVideoCams(msg):
    if (msg.payload ==MQTTServer.payloadAlarmaON):
        globalVars.setSaveVideoCamsOn()
    if (msg.payload ==MQTTServer.payloadAlarmaOFF):
        globalVars.setSaveVideoCamsOff()


def getMQTTAutoTermo(msg):
    if (msg.payload ==MQTTServer.payloadAlarmaON):
        globalVars.setAutoTermoOn()
    if (msg.payload ==MQTTServer.payloadAlarmaOFF):
        globalVars.setAutoTermoOff()


def getMQTTBombaAgua(msg):
    if (msg.payload ==MQTTServer.payloadAlarmaON):
        agua.bombaAguaEncendida()
    if (msg.payload ==MQTTServer.payloadAlarmaOFF):
        agua.bombaAguaApagada()


def getMQTTTimbre(msg):
    toLogFile('Recibido msg Timbre: ' + msg.topic + "@. Payload: @" + str(msg.payload) + "@")
    for i in range(0, globalVars.numRaspis + 1):
	    globalVars.redisRequestSet(globalVars.redisTimbreRequest.replace('X',str(i)))
    globalVars.toFile(globalVars.sendFile, "Atención: están llamando al timbre de la puerta!!")
    foto.photoEntrada()
    globalVars.playAlexaTTS('timbre.sh')


def getMQTTAqaraAlarm(msg):
    s = "getMQTTAqaraAlarm. Topic[-1:] " + msg.topic[-1:] +  " : @" + str(msg.topic) + "@. Payload: @" + str(msg.payload) + "@"
    # toLogFile(s)
    js = json.loads(msg.payload)
    if js['occupancy']:  # AqaraMotion detecta presencia. Hay que comprobar si la alarma está activada para disparar la alerta
        # toLogFile('PRESENCIA!!!!!!')
        if globalVars.isAlarmActive():
            globalVars.fireAlarm(' ALARMA AQARA ' + msg.topic)


def getMQTTHumo(msg):
    try:
        js = json.loads(msg.payload)
        if (js['smoke']) and (js['smoke_density'] >0):  # ATENCIÓN está saltando una alerta de humo!!!!!
            globalVars.fireAlarm(' ALARMA HUMO!!!!!! ' + msg.topic)
        return True
    except Exception as e:
        toLogFile('Error getMQTTHumo: ' + str(e))
        return False


# Para que funcione los comandos de radio deben darse las siguientes condiciones:
# 1-) El proceso MQTTSub debe estar en ejecución en cubieSrv (supervisor)
# 2-) El check "RadioParking" debe estar activado (sergutpal.dynu.com)
# 3-) En la raspi4 debemos tener el USB radio conectado y funcionando correctamente. En caso de cuelgue, hay que hacer un /root/resetUSB.sh
def getMQTTRTL433(msg):
    REPEAT_CMD_SECONDS = 2  # Si llegan nuevos mensajes dentro de los REPEAT_CMD_SECONDS del mensaje anterior procesado, los ignoramos 
    # Esta funcion comprueba que no hayan llegado 2 comandos rtl_433 muy seguidos. En ese caso entendemos que
    # puede deberse a una segunda lectura demasiado rapida y en ese caso ignoramos la segunda cmd
    if globalVars.redisGet(globalVars.redisRTL433IsBusy, False):
        return False

    try:
        toLogFile('Mensaje RTL433 recibido: ')
        js = json.loads(msg.payload)
        id = str(js['id'])
        toLogFile(id)
        if (id ==MQTTServer.payloadRTL433Timbre1) or (id ==MQTTServer.payloadRTL433Timbre2):
            getMQTTTimbre(msg)
        if (id ==MQTTServer.payloadRTL433Parking1) or (id ==MQTTServer.payloadRTL433Parking2) or (id ==MQTTServer.payloadRTL433Parking3) or (id ==MQTTServer.payloadRTL433Parking4):
            if globalVars.getConfigField('radioParking') == '1':
                parkingRequest('0')
                globalVars.toFile(globalVars.sendFile, "Peticion radio abrir parking recibida (" + id + ")")
        if (id ==MQTTServer.payloadRTL433Naranja):
            wakeonlanRequest(False)
            globalVars.toFile(globalVars.sendFile, "Peticion radio WOL (" + id + ")")
        globalVars.redisSet(globalVars.redisRTL433IsBusy, globalVars.redisRTL433IsBusy, REPEAT_CMD_SECONDS)
        return True
    except Exception as e:
        #toLogFile('Error getMQTTRTL433: ' + str(e))
        return False

def getMQTTClick1(msg):
    try:
        action = msg.payload
        if action ==MQTTServer.payloadClickSingle:  # Pulsacion estandard: unica y corta
            wakeonlanRequest(True)
            # globalVars.toFile(globalVars.sendFile, "Click1 simple")
        if action ==MQTTServer.payloadClickDouble:  # Pulsacion doble click
            wakeonlanRequest(True)
            wakeonlanOffRequest()
            # globalVars.toFile(globalVars.sendFile, "Click1 doble click")
        if action ==MQTTServer.payloadClickHold:  # Pulsacion larga
            wakeonlanOffRequest()
            # globalVars.toFile(globalVars.sendFile, "Click1 laaaarga")
        return True
    except Exception as e:
        toLogFile('Error getMQTTClick1: ' + str(e))
        return False


def on_message(mqttc, obj, msg):
    try:
#       s = "MQTTSub msgRecibido. Topic: @" + str(msg.topic) + "@. Payload: @" + str(msg.payload) + "@"
#       toLogFile(s)
       if (msg.topic == MQTTServer.topicParkingOpen) and (msg.payload ==MQTTServer.payloadParkingOpen):
           getMQTTParking(msg)
       if (msg.topic == MQTTServer.topicPuertaParking):
           checkMQTTPuertaParking(msg)
       if msg.topic == MQTTServer.topicAlarma:
           getMQTTAlarma(msg)
       if msg.topic == MQTTServer.topicAlarmaAuto:
           getMQTTAlarmaAuto(msg)
       if msg.topic == MQTTServer.topicRadioParking:
           getMQTTRadioParking(msg)
       if msg.topic == MQTTServer.topicSaveVideoCams:
           getMQTTSaveVideoCams(msg)
       if msg.topic == MQTTServer.topicAutoTermo:
           getMQTTAutoTermo(msg)
       if msg.topic == MQTTServer.topicBombaAgua:
           getMQTTBombaAgua(msg)
       if msg.topic[:-1] == MQTTServer.topicHumo.replace('X', ''):
           getMQTTHumo(msg)
       if (msg.topic == MQTTServer.topicTimbre) and (msg.payload ==MQTTServer.payloadTimbre):
            getMQTTTimbre(msg)
       if msg.topic[:-1] == MQTTServer.topicAqaraMotion.replace('X', ''):
            getMQTTAqaraAlarm(msg)
       if msg.topic[:-1] == MQTTServer.topicAqaraDoor.replace('X', ''):
            getMQTTAqaraAlarm(msg)
       if msg.topic == MQTTServer.topicRTL433:
            getMQTTRTL433(msg)
       if msg.topic == MQTTServer.topicClick1:
            getMQTTClick1(msg)
    except Exception as e:
        # toLogFile('Error on_message: ' + str(e))
        return False



def iniMQTT():
    global mqttc
    global disconnect_flag

    # El "receptor" genérico de mensajes que escucha todo los que se publica, únicamente estará en cubieSrv
    if (globalVars.raspiId =="0") and ((mqttc is None) or disconnect_flag):
        try:
            mqttc = mqtt.Client(client_id="cubieSrvSub", clean_session=True)
            mqttc.on_message = on_message
            mqttc.on_disconnect = on_disconnect
            mqttc.username_pw_set(username=MQTTServer.mqttUser,password=MQTTServer.mqttPwd)
            if (mqttc.connect(MQTTServer.mqttSrv, MQTTServer.mqttPort) !=0):
               raise Exception('MQTTSub no puede conectar con el servidor MQTT')
            mqttc.subscribe(MQTTServer.topicParkingOpen, qos=0)
            mqttc.subscribe(MQTTServer.topicPuertaParking, qos=0)
            mqttc.subscribe(MQTTServer.topicAlarma, qos=0)
            mqttc.subscribe(MQTTServer.topicAlarmaAuto, qos=0)
            mqttc.subscribe(MQTTServer.topicRadioParking, qos=0)
            mqttc.subscribe(MQTTServer.topicSaveVideoCams, qos=0)
            mqttc.subscribe(MQTTServer.topicAutoTermo, qos=0)
            mqttc.subscribe(MQTTServer.topicBombaAgua, qos=0)
            for i in range(1, globalVars.aqaraSmokeNum + 1):
                mqttc.subscribe(MQTTServer.topicHumo.replace('X', str(i)), qos=0)
            mqttc.subscribe(MQTTServer.topicTimbre, qos=0)
            for i in range(1, globalVars.aqaraMotionNum + 1):
                mqttc.subscribe(MQTTServer.topicAqaraMotion.replace('X', str(i)), qos=0)
            for i in range(1, globalVars.aqaraDoorNum + 1):
                mqttc.subscribe(MQTTServer.topicAqaraDoor.replace('X', str(i)), qos=0)
            mqttc.subscribe(MQTTServer.topicEfergy, qos=0)
            mqttc.subscribe(MQTTServer.topicRTL433, qos=0)
            mqttc.subscribe(MQTTServer.topicClick1, qos=0)
            disconnect_flag = False
            toLogFile('MQTTProcess.initMQTT OK')
            return True
        except Exception as e:
            toLogFile('Error initMQTT: ' + str(e))
            return False


def loopMQTT():
    global mqttc

    iniMQTT()
    try:
        if mqttc is not None:
            mqttc.loop_forever()
        return True
    except Exception as e:
        toLogFile('Error loopMQTT: ' + str(e))
        return False



if __name__ == "__main__":
    while True:
        try:
            if not loopMQTT():
                raise Exception("Error en loopMQTT")
        except Exception as e:
            toLogFile('Error main MQTTSub!! ' + str(e))
            #mqttc = None
            #if disconnect_flag:
            mqttc = None
            time.sleep(1)

