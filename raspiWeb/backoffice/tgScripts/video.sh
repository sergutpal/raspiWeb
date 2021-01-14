#!/bin/bash

while :
do
    alarm=$(echo get alarmActive | redis-cli)
    saveVideoCams=$(echo get configsaveVideoCams | redis-cli)

    if [ "$alarm" == "1" ] || [ "$saveVideoCams" == "1" ] ; then
        fecha=$(date +%Y%m%ds_%H%M%S)
        echo $fecha
        /usr/bin/ffmpeg -i rtsp://admin:VTLOZG@192.168.1.220:554 -t 150 -acodec copy -vcodec copy /home/tmp/camEntrada/entrada$fecha.mp4 > /dev/null 2>&1 < /dev/null &
        /usr/bin/ffmpeg -i rtsp://admin:KVHPVD@192.168.1.224:554 -t 150 -acodec copy -vcodec copy /home/tmp/camComedor/salon$fecha.mp4 > /dev/null 2>&1 < /dev/null &
        /usr/bin/ffmpeg -i rtsp://admin:GMHANA@192.168.1.223:554 -t 150 -acodec copy -vcodec copy /home/tmp/camSotano/sotano$fecha.mp4 > /dev/null 2>&1 < /dev/null &
        #/usr/bin/ffmpeg -i rtsp://admin:WTUJDT@192.168.1.222:554 -t 150 -acodec copy -vcodec copy /home/tmp/camTerraza/terraza$fecha.mp4 > /dev/null 2>&1 < /dev/null &

        sleep 153
        mv /home/tmp/camEntrada/entrada$fecha.mp4 /home/tmp/onedrive/cams
        mv /home/tmp/camComedor/salon$fecha.mp4 /home/tmp/onedrive/cams
        mv /home/tmp/camSotano/sotano$fecha.mp4 /home/tmp/onedrive/cams
        #mv /home/tmp/camTerraza/terraza$fecha.mp4 /home/tmp/onedrive/cams
        /home/nfs/telegram/tgScripts/rclone.sh
    fi
done