#!/usr/bin/python

import subprocess
import globalVars


def ecoforest():
    try:
      command = "/home/nfs/telegram/tgScripts/ecoforest.sh"
      subprocess.Popen(command, shell=True)
      globalVars.toFile(globalVars.sendFile, "Mensaje ecoforest enviado")
    except Exception as e:
        toLogFile('Error ecoforest: ' + str(e))
        return False

if __name__ == "__main__":
    ecoforest()
