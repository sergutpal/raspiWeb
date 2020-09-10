#!/bin/sh -e

echo forcefsck > /forcefsck

/home/nfs/telegram/tgScripts/iniTmps.sh

cp /home/nfs/telegram/db/backupEmptyDB/efergy.db /tmp/telegram/efergy.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi1.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi2DHT22.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi3.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi4.db

# /usr/local/bin/noip2 &

#python3 /home/nfs/telegram/tgScripts/telegram.py &

/usr/sbin/ufw enable
#/usr/local/bin/fail2ban-client start

/usr/local/squid/sbin/squid -YC -N -f /etc/squid/squid.conf &

/home/nfs/telegram/tgScripts/iniAll.sh

#find / -name ".nfs000*" -type f -delete  # Borramos todos los ficheros temporales del NFS que se hayan podido quedar residentes
#find /var/log -name "*.gz" -type f -delete
#find /home/imgPi/pi1/var/log -name "*.gz" -type f -delete
#find /home/imgPi/pi2/var/log -name "*.gz" -type f -delete
#find /home/imgPi/pi3/var/log -name "*.gz" -type f -delete
#find /home/imgPi/pi4/var/log -name "*.gz" -type f -delete
#find /home/nfs/telegram/logs -name "*.gz" -type f -delete
rm -rf /home/imgPi/pi1/var/www/cam/media/*
#rm -rf /home/imgPi/pi2/var/www/cam/media/*
rm -rf /home/imgPi/pi3/var/www/cam/media/*
rm -rf /home/imgPi/pi4/var/www/cam/media/*
#truncate --size=0 /home/nfs/telegram/logs/*
#truncate --size=0 /var/log/*
#truncate --size=0 /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/*

chmod 777 -R /var/run/php

echo 0 >/sys/class/leds/led1/brightness
echo 0 >/sys/class/leds/led0/brightness

/home/nfs/telegram/tgScripts/iniPi.sh &

/home/nfs/telegram/gpio/efergy/efergy.sh &

/home/nfs/telegram/tgScripts/firewall.sh

/usr/local/bin/mpc -h 127.0.0.1 -p 6600 clear
/usr/local/bin/mpc -h 127.0.0.1 -p 6600 stop

python3 /home/nfs/telegram/tgScripts/info.py

exit 0
