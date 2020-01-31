#!/usr/bin/python

import globalVars
import sys

if __name__ == "__main__":
    try:
        piNumber = sys.argv[1]
    except Exception as e:
        piNumber = '0'
    globalVars.watchdog(True, piNumber)
