#!/usr/bin/python

import subprocess
import globalVars
import time


def camEntrada(sendFile):
    globalVars.toFile(globalVars.sendFile, "Solicitud preparar video de 30s de la Entrada y enviarlo a DropBox")
    command = globalVars.pathBaseTgScripts + "camEntrada.sh"
    subprocess.Popen(command, shell=True)
    time.sleep(35) # esperamos a que el video acabe de grabarse. MUY IMPORTANTE: el sleep debe estar sincronizado con el tiempo de grabacion que tenemos en el fichero camEntrada.sh
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "MP4 entrada enviado a DropBox")

if __name__ == "__main__":
    camEntrada(True)
