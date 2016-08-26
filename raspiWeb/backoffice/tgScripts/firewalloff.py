#!/usr/bin/python

import globalVars


if __name__ == "__main__":
    globalVars.toFile(globalVars.sendFile, "Peticion Firewall Off")
    globalVars.firewall('off')
    globalVars.fail2ban('off')

