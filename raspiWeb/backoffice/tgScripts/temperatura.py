#!/usr/bin/python

import globalVars
from MQTTSend import pubMQTTMsg
import MQTTServer
import time
import sys


def sendLastTemperatureTelegram():
    pubMQTTMsg(MQTTServer.topicGetTemperaturas, '')


if __name__ == "__main__":
    sendLastTemperatureTelegram()