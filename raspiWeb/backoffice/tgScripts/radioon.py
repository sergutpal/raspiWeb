import MQTTServer
from MQTTSend import pubMQTTMsg


if __name__ == "__main__":
    pubMQTTMsg(MQTTServer.topicRadioParking, MQTTServer.payloadAlarmaON)

