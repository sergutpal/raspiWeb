#!/usr/bin/python

import globalVars

globalVars.getValues(globalVars.pathEfergyDB, 'ENERGIA', 'efergy',
                     'historicoefergy', 'energia', 'W', globalVars.sendFile)
