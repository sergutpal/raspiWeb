#!/usr/bin/python

import time
import subprocess
import globalVars
from MQTTSend import pubMQTTMsg
import MQTTServer


def wakeonlanOffRequest():
    pubMQTTMsg(MQTTServer.topicWOLPC, MQTTServer.payloadPCOFF)


if __name__ == "__main__":
    wakeonlanOffRequest()
