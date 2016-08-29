#!/bin/bash

ntpd -gq

#mount -a

echo 0 >/sys/class/leds/led1/brightness
echo 0 >/sys/class/leds/led0/brightness

#START RASPIMJPEG SECTION
mkdir -p /dev/shm/mjpeg
chown www-data:www-data /dev/shm/mjpeg
chmod 777 /dev/shm/mjpeg
sleep 4;su -c 'raspimjpeg > /dev/null 2>&1 &' www-data
#if [ -e /etc/debian_version ]; then
  sleep 4;su -c "php /var/www/cam/schedule.php > /dev/null 2>&1 &" www-data
#else
#  sleep 4;su -s '/bin/bash' -c "php /var/www/cam/schedule.php > /dev/null 2>&1 &" www-data
#fi
# Arrancamos el proceso, pero paramos la camara para que no grave hasta que se lo indiquemos
echo "ru 0" > /var/www/cam/FIFO
#END RASPIMJPEG SECTION

python /home/nfs/telegram/gpio/pir/pir.py &

/home/nfs/telegram/tgScripts/iniAll.sh

host=$(</etc/hostname)
if [ $host = "raspi2" ]; then
	#/usr/local/bin/mpc clear
	/usr/local/bin/mpc stop
fi


exit 0

