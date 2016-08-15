#!/bin/bash

#echo "Ejecutado dhcpevent.sh " $1 ". " $2 ". " $3 ". " $4 >> /home/tmp/telegram/log.txt
python /home/nfs/telegram/tgScripts/dhcpevent.py $1 $2 $3 $4
exit $?
