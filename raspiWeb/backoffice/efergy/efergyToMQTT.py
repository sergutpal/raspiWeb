#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import json
import sqlite3
import globalVars
from time import sleep
import datetime
from MQTTSend import pubMQTTMsg


def sendEfergyToMQTT():
    try:
        try:
            DB = sqlite3.connect(globalVars.pathEfergyDB)
            cur = DB.cursor()
            e = globalVars.getActualValue(cur, 'efergy', 'energia', '', False)
            energia = e.get('value')
        except Exception as e:
            globalVars.toLogFile('Error efergyToMQTT obteniendo efergy from sqlite: ' + str(e))
            energia = ''
        finally:
            cur.close()
            DB.close()
        efergy = {"efergy": round(float(energia), 2)}
        js = json.dumps(efergy)
        pubMQTTMsg("efergy", js)
    except Exception as e:
        globalVars.toLogFile('Error sendEfergyToMQTT: ' + str(e))
        return False
    finally:
        return True


if __name__ == "__main__":
    sendEfergyToMQTT()
