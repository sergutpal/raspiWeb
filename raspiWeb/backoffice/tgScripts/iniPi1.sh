#!/bin/bash

#python /home/nfs/telegram/gpio/pir/pir.py &

host=$(</etc/hostname)

echo 0 >/sys/class/leds/led1/brightness
echo 0 >/sys/class/leds/led0/brightness

/home/nfs/telegram/tgScripts/iniAll.sh

ntpd -gq

exit 0

