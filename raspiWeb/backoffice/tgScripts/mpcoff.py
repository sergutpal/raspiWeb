#!/usr/bin/python

import subprocess
import globalVars


def stopMusic(sendTelegram):
    command = "/usr/local/bin/mpc stop -h 127.0.0.1 -p 6601"
    subprocess.Popen(command, shell=True)
    if (sendTelegram):
        globalVars.toFile(globalVars.sendFile, "mpc STOP")
    return True

if __name__ == "__main__":
    stopMusic(True)
