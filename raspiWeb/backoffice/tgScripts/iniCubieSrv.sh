#!/bin/sh -e

mkdir /tmp/telegram
chmod 777 /tmp/telegram

mkdir /tmp/telegram/RpiCam
chmod 777 /tmp/telegram

echo forcefsck > /forcefsck

cp /home/nfs/telegram/db/backupEmptyDB/efergy.db /tmp/telegram/efergy.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi1.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi2DHT22.db
cp /home/nfs/telegram/db/backupEmptyDB/temperaturaraspi.db /tmp/telegram/temperaturaraspi3.db

/usr/local/bin/noip2 &

# /usr/sbin/ufw enable

#/home/nfs/telegram/telegram-cli/bin/telegram-cli -k /home/nfs/telegram/telegram-cli/tg-server.pub -W -s /home/nfs/telegram/tgScripts/rpicontrol.lua -U root -P 8009 -d -vvvRC &
#sleep 1
#/usr/local/bin/rtl_fm -f 433505000 -s 200000 -r 96000 -A fast -p 60 -g 49.6 2>/dev/null | /home/nfs/raspiWeb/raspiWeb/backoffice/efergy/efergy &

# sleep 10
python /home/nfs/telegram/tgScripts/telegram.py &

/usr/local/bin/mpc -h 127.0.0.1 -p 6601 clear
/usr/local/bin/mpc -h 127.0.0.1 -p 6601 stop

/home/nfs/telegram/tgScripts/iniAll.sh

python /home/nfs/telegram/tgScripts/info.py

exit 0
