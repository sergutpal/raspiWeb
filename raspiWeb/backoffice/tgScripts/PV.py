#!/usr/bin/env python3

import json
import time
import globalVars
import MQTTServer
from MQTTSend import pubMQTTMsg
from pygoodwe import SingleInverter

gw = None

def initPV():
  global gw

  args = {
    'gw_station_id' : '6dd7a391-7003-4598-aba3-a80ef04a7a24',
    'gw_account' : 'sergutpal@hotmail.com',
    'gw_password' : 'Goodwe2018',
  }

  try:
    gw = SingleInverter(
        system_id=args.get('gw_station_id', '1'),
        account=args.get('gw_account', 'thiswillnotwork'),
        password=args.get('gw_password', 'thiswillnotwork'),
        )
    # print(gw.data.keys())
    # print(gw.data.get('kpi'))
    # print(gw.data.get('energeStatisticsCharts'))
    return True
  except Exception as e:
    globalVars.toLogFile('Error initPV: ' + str(e))
    return False


def getPV():
  global gw

  while (1 == 1):
    try:
      gw.getCurrentReadings()
      PVNow = gw.data.get('kpi').get('pac')
      PVSumToday = gw.data.get('kpi').get('power')
      print('PVNow: ' +str(PVNow) + '. PV Today: ' + str(PVSumToday))
      pvjson = json.dumps({'PVNow': PVNow, 'PVSumToday': PVSumToday})
      pubMQTTMsg(MQTTServer.topicPV, pvjson)
      globalVars.redisSet(globalVars.redisPVNow, PVNow)  # float(globalVars.redisGet(globalVars.redisPVNow))
      globalVars.redisSet(globalVars.redisPVSumToday, PVSumToday)  # float(globalVars.redisGet(globalVars.redisPVSumToday))
      time.sleep(60)
    except Exception as e:
      globalVars.toLogFile('Error PV: ' + str(e))


if __name__ == "__main__":
    if initPV():
      getPV()
    else:
      globalVars.toLogFile('Error: no se ha podido inicializar el módulo PV!')