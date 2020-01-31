#!/usr/bin/python

import subprocess
import globalVars


def wakeonlanRequest(sendFile):
    command = "/usr/bin/wakeonlan b0:6e:bf:c3:bc:22"
    subprocess.Popen(command, shell=True)
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "Wakeonlan PC")

if __name__ == "__main__":
    wakeonlanRequest(True)
