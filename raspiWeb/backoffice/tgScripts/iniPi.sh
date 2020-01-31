#!/bin/bash

#python /home/nfs/telegram/gpio/pir/pir.py &

#START RASPIMJPEG SECTION
mkdir -p /dev/shm/mjpeg
chown www-data:www-data /dev/shm/mjpeg
chmod 777 -R /dev/shm/mjpeg
sleep 4
raspimjpeg > /dev/null 2>&1 &
sleep 4
php /var/www/cam/schedule.php > /dev/null 2>&1 &
# Arrancamos el proceso, pero paramos la camara para que no grave hasta que se lo indiquemos
#chmod 777 /dev/shm/mjpeg/*
echo "ru 0" > /var/www/cam/FIFO
#END RASPIMJPEG SECTION

host=$(</etc/hostname)

echo 0 >/sys/class/leds/led1/brightness
echo 0 >/sys/class/leds/led0/brightness

/home/nfs/telegram/tgScripts/iniAll.sh

ntpd -gq

exit 0

