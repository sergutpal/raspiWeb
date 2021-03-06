#!/bin/sh -e

[ -d "/tmp/telegram" ] && rm -rf /tmp/telegram
mkdir /tmp/telegram
mkdir /tmp/telegram/RpiCam
mkdir /tmp/telegram/logs

[ -d "/tmp/dropbox" ] && rm -rf /tmp/dropbox
mkdir /tmp/dropbox
mkdir /tmp/dropbox/backup
mkdir /tmp/dropbox/ping
mkdir /tmp/dropbox/camEntrada
mkdir /tmp/dropbox/camComedor
mkdir /tmp/dropbox/video
mkdir /tmp/camEntrada
mkdir /tmp/camComedor
mkdir /tmp/camSotano
mkdir /tmp/camTerraza
mkdir /tmp/onedrive
mkdir /tmp/onedrive/cams

chmod -R 777 /tmp/telegram
chmod -R 777 /tmp/dropbox
chmod -R 777 /tmp/camEntrada
chmod -R 777 /tmp/camComedor
chmod -R 777 /tmp/camEntrada
chmod -R 777 /tmp/camSotano
chmod -R 777 /tmp/camTerraza
chmod -R 777 /tmp/onedrive

exit 0
