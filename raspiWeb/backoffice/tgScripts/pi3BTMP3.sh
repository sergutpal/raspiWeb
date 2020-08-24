#!/bin/bash

echo -e "connect 0C:EE:99:F7:D6:B6 " | bluetoothctl

sleep 5

aplay -D bluealsa:SRV=org.bluealsa,DEV=0C:EE:99:F7:D6:B6,PROFILE=a2dp /home/nfs/mp3/alarma.wav

echo -e "disconnect 0C:EE:99:F7:D6:B6" | bluetoothctl

exit $?
