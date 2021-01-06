#!/usr/bin/python

import subprocess
import globalVars


def airesOff():
    try:
      command = "/home/nfs/telegram/tgScripts/airesoff.sh"
      subprocess.Popen(command, shell=True)
      globalVars.toFile(globalVars.sendFile, "Mensaje aires OFF enviado")
    except Exception as e:
        toLogFile('Error airesOn: ' + str(e))
        return False

if __name__ == "__main__":
    airesOff()
