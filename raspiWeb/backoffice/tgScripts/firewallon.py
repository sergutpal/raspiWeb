#!/usr/bin/python

import globalVars


if __name__ == "__main__":
    globalVars.toFile(globalVars.sendFile, "Peticion Firewall ON")
    globalVars.firewall('on')
    globalVars.fail2ban('on')
