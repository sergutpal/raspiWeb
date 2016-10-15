#!/bin/bash

python /home/nfs/telegram/gpio/pir/pir.py &

#START RASPIMJPEG SECTION
mkdir -p /dev/shm/mjpeg
chown www-data:www-data /dev/shm/mjpeg
chmod 777 /dev/shm/mjpeg
sleep 4;su -c 'raspimjpeg > /dev/null 2>&1 &' www-data
sleep 4;su -c "php /var/www/cam/schedule.php > /dev/null 2>&1 &" www-data
# Arrancamos el proceso, pero paramos la camara para que no grave hasta que se lo indiquemos
echo "ru 0" > /var/www/cam/FIFO
#END RASPIMJPEG SECTION

host=$(</etc/hostname)
if [ $host = "raspi2" ]; then
	#/usr/local/bin/mpc clear
	/usr/local/bin/mpc stop
fi

echo 0 >/sys/class/leds/led1/brightness
echo 0 >/sys/class/leds/led0/brightness

/home/nfs/telegram/tgScripts/iniAll.sh

ntpd -gq

exit 0

