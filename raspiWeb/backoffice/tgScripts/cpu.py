#!/usr/bin/python

import globalVars
import psutil
import datetime
import sqlite3
import subprocess
import ip

# command = "echo | vcgencmd measure_temp >> " + globalVars.sendFile;
# process = subprocess.Popen(command, shell = True);


def writeInfo():
    try:
        if (globalVars.isNightModeActive()):
            txt = 'La alarma esta en modo NOCHE. '
        else:
            if (globalVars.isAlarmActive()):
                txt = 'La alarma esta ACTIVADA. '
            else:
                txt = 'La alarma esta desactivada. '
        if (globalVars.isAlarmAuto()):
            txt = txt + 'Alarma: Modo automatico activado. '
        else:
            txt = txt + 'Alarma: Modo automatico desactivado. '
        if globalVars.isParkingOpen():
            txt = txt + 'Parking abierto. '
        else:
            txt = txt + 'Parking cerrado. '
        try:
            DB = sqlite3.connect(globalVars.pathEfergyDB)
            cur = DB.cursor()
            energia = globalVars.getActualValue(cur, 'efergy', 'energia', ' W')
        except Exception as e:
            globalVars.toLogFile('Error writeInfo: ' + str(e))
            energia = ''
        finally:
            cur.close()
            DB.close()
        txt = txt + 'Energia: ' + energia + '. '
        txt = txt + '%CPU: ' + \
            str(psutil.cpu_percent(interval=1, percpu=False)) + '%'
        psutil.virtual_memory()
        # txt = txt + '. Mem Total: ' + str(psutil.virtual_memory()[0])
        # txt = txt + '. Mem Disponible: ' + str(psutil.virtual_memory()[1])
        txt = txt + '. %Mem Usada: ' + str(psutil.virtual_memory()[2]) + '%'
        diskUsage = psutil.disk_usage('/')
        txt = txt + '. %Uso root: ' + str(diskUsage[3]) + '%'
        diskUsage = psutil.disk_usage(globalVars.pathBase)
        txt = txt + '. %Uso nfs: ' + str(diskUsage[3]) + '%'
        bootime = psutil.boot_time()
        txt = txt + '. Boottime: ' + \
            datetime.datetime.fromtimestamp(
                bootime).strftime('%d/%m/%y %H:%M:%S')
        print(txt)
    except Exception as e:
        txt = 'Error writeInfo: ' + str(e)
    finally:
        globalVars.toFile(globalVars.sendFile, txt)


if __name__ == "__main__":
    writeInfo()
    #globalVars.firewall('status')
    #ip = ip.get_ip_public()
    #globalVars.toFile(globalVars.sendFile, "IP publica: " + ip)

