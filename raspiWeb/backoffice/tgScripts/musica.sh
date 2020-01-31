#!/bin/bash

if [ ! -z "$1" ]; then
    /usr/bin/supervisorctl stop mpd
    /usr/bin/supervisorctl start mpd
    /usr/bin/supervisorctl stop icecast
    /usr/bin/supervisorctl start icecast
fi
/usr/bin/mpc clear
/usr/bin/mpc add http://ice4.somafm.com/7soul-128-mp3
/usr/bin/mpc add http://ice2.somafm.com/u80s-128-mp3
/usr/bin/mpc add https://streamingv2.shoutcast.com/89fm-sp
/usr/bin/mpc add http://66.70.187.44:9146/stream
/usr/bin/mpc add http://185.33.21.112:80/costadelmarchillout_128
/usr/bin/mpc add http://91.121.155.204:8097/stream
/usr/bin/mpc add http://listen.radionomy.com:80/1HITS80s
/usr/bin/mpc add http://ice4.somafm.com/gsclassic-128-mp3
/usr/bin/mpc add http://ice4.somafm.com/poptron-128-mp3
#/usr/bin/mpc add http://hitfm.es.audio1.glb.ipercast.net:8000/kissfm.es/mp3
#/usr/bin/mpc add http://195.55.74.211/cope/rockfm.mp3
#/usr/bin/mpc add http://195.10.2.95/flaix/shoutcastmp3.mp3
#/usr/bin/mpc add http://208.92.53.92:443/CADENADIAL_SC
#/usr/bin/mpc add http://77.67.34.11:443/LOS40_SC
#/usr/bin/mpc add http://catradio.ccma.audioemotion.stream.flumotion.com/ccma/catradio.mp3
/usr/bin/mpc play

