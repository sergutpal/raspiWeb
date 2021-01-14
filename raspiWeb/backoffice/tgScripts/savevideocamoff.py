import MQTTServer
from MQTTSend import pubMQTTMsg


if __name__ == "__main__":
    pubMQTTMsg(MQTTServer.topicSaveVideoCams, MQTTServer.payloadAlarmaOFF)

