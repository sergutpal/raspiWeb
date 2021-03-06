#!/usr/bin/python

import time
import globalVars


def msgHelp(txt):
    globalVars.toFile(globalVars.sendFile, txt)
    time.sleep(0.7)


def sendHelp():
    msgHelp("Principales comandos que acepta Telegram Raspi:")
    msgHelp("abreparking: abre la puerta del parking")
    msgHelp("alarmaon: activa la alarma")
    msgHelp("alarmaoff: desactiva la alarma")
    msgHelp("calderaon: enciende la caldera")
    msgHelp("calderaoff: apaga la caldera")
    msgHelp("ecoforest / ecoforest2: enciende, o apaga si está encendida, la estufa del salón")
    msgHelp("aires / aireson: enciende los AC de salón y pasillo")
    msgHelp("airesoff: apaga los AC de salón y pasillo")
    msgHelp("termoon: enciende el termo")
    msgHelp("termooff: apaga el termo")
    msgHelp("auto: activa el modo AUTO de la alarma")
    msgHelp("autooff: desactiva el modo AUTO de la alarma")
    msgHelp("autotermoon: activa el modo automático del termo")
    msgHelp("autotermooff: desactiva el modo automático del termo")
    msgHelp("foto: envia una foto de cada una de las camaras")
    msgHelp("cam: activa las camaras de las raspis")
    msgHelp("camoff: desactiva las camaras de las raspis")
    msgHelp("camentrada: graba y envia a Dropbox un video de 30 segundos de la puerta de Entrada")
    msgHelp("camcomedor: graba y envía a Dropbox un video de 30 segundos del comedor")
    msgHelp("savevideocamon: graba las cámaras Ezviz y sube los ficheros a OneDrive")
    msgHelp("savevideocamoff: para la grabación de las cámaras Ezviz")
    msgHelp("video: graba y envía a Dropbox un video de 60 segundos de todas las cámaras")
    msgHelp("on: activa el modo alarma")
    msgHelp("off: desactiva el modo alarma")
    msgHelp("fwoff: desactiva el firewall para permitir el acceso externo. Esta opción DEBE ser de uso exclusivo para casos de emergencia!")
    msgHelp("fw: activa el firewall")
    msgHelp("vpn: desactiva el firewall del puerto de la VPN (49001) para permitir el acceso")
    msgHelp("vpnoff: cierra el puerto de la vpn")
    msgHelp("musica: activa el MPD para escuchar la musica")
    msgHelp("musicaoff: desactiva el MPD")
    msgHelp("wol: enciende el PC (activando el sonoff)")
    msgHelp("woloff: apaga el PC (desactivando el sonoff)")
    msgHelp("radioon: habilita las ordenes de radio (abrir parking, ...)")
    msgHelp("radiooff: desactiva las ordenes de radio (abrir el parking, ...)")
    msgHelp("t: envia las temperaturas al canal raspiBot")
    msgHelp("flush: elimina todas las entradas de Redis")
    msgHelp("info: envia un resumen de los principales parametros")
    msgHelp("agua: enciende la bomba del agua y corta el agua de la general con la electroválvula. En X minutos se apagará de forma automática el agua")
    msgHelp("aguaoff: apaga la bomba de agua siempre que no esté activo el modo emergencia")
    msgHelp("aguanoauto: enciende la bomba del agua, y corta el agua de la general con la electroválvula, pero NO apaga de forma automática la bomba.")
#    msgHelp("**********************")
#    msgHelp("CMD MQTT en RaspiBot:")
#    msgHelp("mqtt wake iconia/hpslate")

if __name__ == "__main__":
    sendHelp()
