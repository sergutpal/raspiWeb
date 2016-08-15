'phone' + str(i)#!/usr/bin/python

import time
import sendmail
from datetime import datetime
from email.utils import COMMASPACE
import globalVars

try:
    globalVars.getTelegramTo();
    print 'TelegramTo: ' +globalVars.tgDestination;
    print 'TelegramToAll: ' +globalVars.tgDestinationAll;
    for i in range (1, 4):
      callPhone = globalVars.getConfigField('phone' + str(i));
      if callPhone:
        print('CallPhone: ' + callPhone);
        #globalVars.callPhone(callPhone);
    sendTo = globalVars.getConfigField('mail');
    print('mailTo: ' +sendTo);

    buzzerTimes = globalVars.getConfigField('buzzerTimes');
    print('buzzerTimes: ' +str(buzzerTimes));
    #if sendTo:
      #sendmail.send_mail(sendTo, 'Probando callTest', None, 'Prueba envio de mail');
except Exception as e:
  print(globalVars.dateTime() + 'Error: ' + str(e) + '\n');


