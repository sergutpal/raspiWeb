#!/usr/bin/python

import subprocess
import globalVars


def firewallVPNOff(sendFile):
    command = globalVars.pathBaseTgScripts + "vpnoff.sh"
    subprocess.Popen(command, shell=True)
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "FWL VP_N Cerrado. Bien hecho!. Recuerda que la activacion del FWL tarda un par de minutos")

if __name__ == "__main__":
    firewallVPNOff(True)
