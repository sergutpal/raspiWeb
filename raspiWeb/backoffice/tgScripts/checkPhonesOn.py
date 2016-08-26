import nmap
import time
import globalVars


def isAnyMobilePhoneOn():
    try:
        hostsTxt = ''
        IP = globalVars.getConfigField('IPAuto1')
        if IP:
            hostsTxt = IP
        IP = globalVars.getConfigField('IPAuto2')
        if IP:
            hostsTxt = hostsTxt + ' ' + IP
        IP = globalVars.getConfigField('IPAuto3')
        if IP:
            hostsTxt = hostsTxt + ' ' + IP
        nm = nmap.PortScanner()
        nm.scan(hosts=hostsTxt, arguments='-sn')
        print 'Cmd: ' + nm.command_line()
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        anyUp = False
        for host, status in hosts_list:
            anyUp = True
            # print('{0}:{1}'.format(host, status))
        return anyUp
    except Exception as e:
        print e
        globalVars.toLogFile('Error isAnyMobilePhoneOn: ' + str(e))
        return False  # En caso de excepcion, activamos la alarma


def checkModeAuto():
    MAX_CHECKS = 30
    WAIT_CHECK = 2

    try:
        if (globalVars.isAlarmAuto()) and (not globalVars.isAlarmActive()):
            isAnyOn = False
            i = 0
            while (not isAnyOn) and (i < MAX_CHECKS):
                isAnyOn = isAnyMobilePhoneOn()
                i = i + 1
                time.sleep(WAIT_CHECK)
            if not isAnyOn:
                globalVars.setAlarm(True)
                globalVars.toFile(globalVars.sendFileToAll,
                                  "Alarma ACTivada automaticamente")
                return True
        else:
            return False
    except Exception as e:
        globalVars.toLogFile('Error checkModeAuto: ' + str(e))
        return False


if checkModeAuto():
    globalVars.toLogFile('Alarma activada automaticamente por checkPhonesOn')
