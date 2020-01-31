#!/usr/bin/python

import subprocess
import globalVars


def firewallVPNOn(sendFile):
    command = globalVars.pathBaseTgScripts + "vpn.sh"
    subprocess.Popen(command, shell=True)
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "FWL abierto para la conexion VP_N. Recuerda cerrar el puerto al acabar enviando vpnoff")

if __name__ == "__main__":
    firewallVPNOn(True)
