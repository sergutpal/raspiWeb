# -*- coding: utf-8 -*-

import globalVars
import sys


def supervisor(cmd, start):
    globalVars.supervisor(cmd, start)
    globalVars.toFile(globalVars.sendFile, 'Ejecutando: ' + start + ' ' + cmd)
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        globalVars.toLogFile('Error supervisor: debes indicar ' +
                             'la acción y el comando')
        exit(0)
    try:
        action = sys.argv[1].lower()
        print 'action: ' + action
        cmd = sys.argv[2].lower()
        print 'cmd: ' + cmd
        if (action):
            if (action == 'start'):
                start = True
            else:
                start = False
        else:
            start = False
    except Exception as e:
        start = False
    supervisor(cmd, start)
