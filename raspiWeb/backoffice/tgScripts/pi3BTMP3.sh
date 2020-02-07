#!/bin/bash

echo -e "connect F8:54:B8:C5:01:D7 " | bluetoothctl

sleep 5

aplay -D bluealsa:SRV=org.bluealsa,DEV=F8:54:B8:C5:01:D7,PROFILE=a2dp /home/nfs/mp3/alarma.wav

echo -e "disconnect F8:54:B8:C5:01:D7" | bluetoothctl

exit $?
