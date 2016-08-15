#!/usr/bin/python

import subprocess
import globalVars


def wakeonlanRequest(sendFile):
    command = "/usr/bin/wakeonlan 2c:56:dc:d3:3c:38"
    subprocess.Popen(command, shell=True)
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "Wakeonlan PC")

if __name__ == "__main__":
    wakeonlanRequest(True)
