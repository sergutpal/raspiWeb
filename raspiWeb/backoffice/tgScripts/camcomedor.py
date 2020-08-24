#!/usr/bin/python

import subprocess
import globalVars
import time

def camComedor(sendFile):
    globalVars.toFile(globalVars.sendFile, "Solicitud preparar video de 30s del Comedor y enviarlo a DropBox")
    command = globalVars.pathBaseTgScripts + "camComedor.sh"
    subprocess.Popen(command, shell=True)
    time.sleep(35) # esperamos a que el video acabe de grabarse. MUY IMPORTANTE: el sleep debe estar sincronizado con el tiempo de grabacion que tenemos en el fichero camComedor.sh
    if sendFile:
        globalVars.toFile(globalVars.sendFile, "MP4 comedor enviado a DropBox")

if __name__ == "__main__":
    camComedor(True)
