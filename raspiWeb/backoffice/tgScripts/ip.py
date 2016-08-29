# -*- coding: utf-8 -*-

import globalVars
from urllib2 import urlopen


def get_ip_public():
    try:
        ip = urlopen('http://ip.42.pl/raw').read()
        return ip
    except Exception as e:
        globalVars.toLogFile('Error get_ip_public: ' + str(e))
        return ''


if __name__ == "__main__":
    ip = get_ip_public()
    globalVars.toFile(globalVars.sendFile, "IP publica: " + ip)
