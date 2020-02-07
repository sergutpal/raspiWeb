#!/bin/bash

set +e

find / -name ".nfs000*" -type f -delete  # Borramos todos los ficheros temporales del NFS que se hayan podido quedar residentes
find /var/log -name "*.gz" -type f -delete
find /home/imgPi/pi1/var/log -name "*.gz" -type f -delete
#find /home/imgPi/pi2/var/log -name "*.gz" -type f -delete
find /home/imgPi/pi3/var/log -name "*.gz" -type f -delete
find /home/imgPi/pi4/var/log -name "*.gz" -type f -delete
find /home/nfs/telegram/logs -name "*.gz" -type f -delete

rm -rf /home/imgPi/pi1/var/www/cam/media/*
#rm -rf /home/imgPi/pi2/var/www/cam/media/*
rm -rf /home/imgPi/pi3/var/www/cam/media/*
rm -rf /home/imgPi/pi4/var/www/cam/media/*

truncate --size=0 /home/nfs/telegram/logs/*
truncate --size=0 /var/log/*
truncate --size=0 /home/tmp/*.log
truncate --size=0 /home/tmp/telegram/logs/*

truncate --size=0 /home/imgPi/pi1/var/log/*
truncate --size=0 /home/imgPi/pi3/var/log/*
truncate --size=0 /home/imgPi/pi4/var/log/*

truncate --size=0 /home/imgPi/pi1/var/log/zigbee2mqtt/*
truncate --size=0 /home/imgPi/pi3/var/log/zigbee2mqtt/*
truncate --size=0 /home/imgPi/pi4/var/log/zigbee2mqtt/*

truncate --size=0 /home/imgPi/pi1/var/log/apt/*
truncate --size=0 /home/imgPi/pi3/var/log/apt/*
truncate --size=0 /home/imgPi/pi4/var/log/apt/*

rm -rf /home/nfs/tmp/ToDelete/*

echo "Todo limpio ;-). Recuerda eliminar todos los firmwares de raspis que no se utilicen en /lib/modules" > /home/tmp/telegram/send.txt

exit 0
