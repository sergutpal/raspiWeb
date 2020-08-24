#!/usr/bin/python

import os
import time
from datetime import datetime
import subprocess
import shutil
import globalVars

# from pycall import CallFile, Call, Application

def callPhoneAlarm():
    if globalVars.getConfigField('alarmPhoneActive') =='1':
        for i in range(1, 4):
            callPhone = globalVars.getConfigField('phone' + str(i))
            if callPhone:
                globalVars.callPhone(callPhone)
                time.sleep(90)  # Esperamos 90s entre cada llamada para asegurarnos que la linea principal esté libre


