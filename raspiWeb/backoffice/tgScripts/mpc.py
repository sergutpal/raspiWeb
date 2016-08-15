#!/usr/bin/python

import subprocess
import globalVars


def playMusic(sendTelegram):
    command = globalVars.pathBaseTgScripts + "musica.sh"
    subprocess.Popen(command, shell=True)

    if sendTelegram:
        globalVars.toFile(globalVars.sendFile, "mpc PLAYing")
    return True

if __name__ == "__main__":
    playMusic(True)
