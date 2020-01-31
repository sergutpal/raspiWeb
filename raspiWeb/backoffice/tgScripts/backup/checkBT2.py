#!/usr/bin/python

import bluetooth
import time

print ("In/Out Board")

while True:
    print ("Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))

    result = bluetooth.lookup_name('BC:E2:65:43:1C:10', timeout=5)
    if (result != None):
        print ("SGP: in")
    else:
        print ("SGP: out")

    result = bluetooth.lookup_name('54:25:EA:76:23:8E', timeout=5)
    if (result != None):
        print ("CAOC: in")
    else:
        print ("CAOC: out")

    time.sleep(60)

