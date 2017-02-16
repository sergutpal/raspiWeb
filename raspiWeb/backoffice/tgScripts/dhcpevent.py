#!/usr/bin/python

import globalVars
import sys
import getopt


def main(argv):
    try:
        globalVars.toLogFile(globalVars.dateTime() +'Ejecucion dhcpevent.');
        opts, args = getopt.getopt(argv, '')
        if len(args) < 2:
            sys.exit(2)
        if not (args[0].lower() == 'commit'):
            sys.exit(0)
        IPEvent = args[1]
        # globalVars.toLogFile(globalVars.dateTime() +'dhcpevent.py: ' +
        #                      args[0] + '. ' + args[1]);
        if IPEvent and ((globalVars.getConfigField('IPAuto1') == IPEvent) or
                        (globalVars.getConfigField('IPAuto2') == IPEvent) or
                        (globalVars.getConfigField('IPAuto3') == IPEvent)):
            # if (globalVars.isAlarmActive() and globalVars.isAlarmAuto()):
            if (globalVars.isAlarmActive()):
                globalVars.setAlarm(False)
                globalVars.toFile(globalVars.sendFileToAll,
                                  "Alarma desactivada automaticamente")
                globalVars.toLogFile(
                    "Alarma desactivada automaticamente por dhcpevent.py")
    except getopt.GetoptError as e:
        globalVars.toLogFile('Error parametros dhcpevent: ' + str(e))
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
