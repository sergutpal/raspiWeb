#!/usr/bin/python

import time
import globalVars


def msgHelp(txt):
    globalVars.toFile(globalVars.sendFile, txt)
    time.sleep(0.7)


def sendHelp():
    msgHelp("Principales comandos que acepta Telegram Raspi:")
    msgHelp("auto: activa el modo AUTO de la alarma")
    msgHelp("autooff: desactiva el modo AUTO de la alarma")
    msgHelp("cam: activa las camaras de las raspis")
    msgHelp("camoff: desactiva las camaras de las raspis")
    msgHelp("on: activa el modo alarma")
    msgHelp("off: desactiva el modo alarma")
    msgHelp("fwoff: desactiva el firewall para permitir el acceso externo. Esta opción DEBE ser de uso exclusivo para casos de emergencia!")
    msgHelp("fw: activa el firewall")
    msgHelp("vpn: desactiva el firewall del puerto de la VPN (49001) para permitir el acceso")
    msgHelp("vpnoff: cierra el puerto de la vpn")
    msgHelp("musica: activa el MPD para escuchar la musica")
    msgHelp("musicaoff: desactiva el MPD")
    msgHelp("**********************")
    msgHelp("CMD MQTT en RaspiBot:")
    msgHelp("mqtt wake iconia/hpslate")

if __name__ == "__main__":
    sendHelp()
