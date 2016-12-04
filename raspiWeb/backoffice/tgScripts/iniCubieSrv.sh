#!/bin/sh -e

mkdir /tmp/telegram
mkdir /tmp/telegram/RpiCam
mkdir /tmp/dropbox
mkdir /tmp/dropbox/backup
mkdir /tmp/dropbox/ping

echo forcefsck > /forcefsck

cp /home/nfs/telegram/db/backupEmptyDB/efergy.db /tmp/telegram/efergy.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi1.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi2DHT22.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi3.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi4.db

chmod -R 777 /tmp/telegram

# /usr/local/bin/noip2 &

python /home/nfs/telegram/tgScripts/telegram.py &

/usr/sbin/ufw enable
/usr/local/bin/fail2ban-client start

python /home/nfs/telegram/tgScripts/info.py

/home/nfs/telegram/tgScripts/iniAll.sh

#/usr/local/bin/mpc -h 127.0.0.1 -p 6601 clear
#/usr/local/bin/mpc -h 127.0.0.1 -p 6601 stop

find / -name ".nfs000*" -type f -delete  # Borramos todos los ficheros temporales del NFS que se hayan podido quedar residentes
find /var/log -name "*.gz" -type f -delete
find /home/imgPi/pi1/var/log -name "*.gz" -type f -delete
find /home/imgPi/pi2/var/log -name "*.gz" -type f -delete
find /home/imgPi/pi3/var/log -name "*.gz" -type f -delete
find /home/imgPi/pi4/var/log -name "*.gz" -type f -delete
find /home/nfs/telegram/logs -name "*.gz" -type f -delete
host=$(</etc/hostname)
iniFile="/home/nfs/telegram/logs/ini$host.log"
echo CubieSrvOK >> $iniFile
exit 0

