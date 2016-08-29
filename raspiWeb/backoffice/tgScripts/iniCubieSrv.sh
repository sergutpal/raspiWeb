#!/bin/sh -e

mkdir /tmp/telegram
mkdir /tmp/telegram/RpiCam

echo forcefsck > /forcefsck

cp /home/nfs/telegram/db/backupEmptyDB/efergy.db /tmp/telegram/efergy.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi1.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi2DHT22.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi3.db

chmod -R 777 /tmp/telegram

# /usr/local/bin/noip2 &

python /home/nfs/telegram/tgScripts/telegram.py &

/usr/sbin/ufw enable
/usr/local/bin/fail2ban-client start

python /home/nfs/telegram/tgScripts/info.py

/home/nfs/telegram/tgScripts/iniAll.sh

#/usr/local/bin/mpc -h 127.0.0.1 -p 6601 clear
#/usr/local/bin/mpc -h 127.0.0.1 -p 6601 stop

exit 0
