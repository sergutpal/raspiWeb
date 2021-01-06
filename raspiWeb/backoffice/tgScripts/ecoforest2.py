#!/usr/bin/python

import subprocess
import globalVars


def ecoforest():
    command = "/home/nfs/telegram/tgScripts/ecoforest2.sh"
    subprocess.Popen(command, shell=True)
    globalVars.toFile(globalVars.sendFile, "Mensaje ecoforest enviado")

if __name__ == "__main__":
    ecoforest()
