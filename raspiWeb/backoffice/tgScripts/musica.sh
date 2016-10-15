#!/bin/bash

if [ ! -z "$1" ]; then
    /usr/bin/supervisorctl stop mpd
    /usr/bin/supervisorctl start mpd
    /usr/bin/supervisorctl stop icecast
    /usr/bin/supervisorctl start icecast
fi
/usr/local/bin/mpc clear
/usr/local/bin/mpc add http://hitfm.es.audio1.glb.ipercast.net:8000/kissfm.es/mp3
/usr/local/bin/mpc add http://195.55.74.211/cope/rockfm.mp3
/usr/local/bin/mpc add http://listen.radionomy.com:80/1HITS80s
/usr/local/bin/mpc add http://195.10.2.95/flaix/shoutcastmp3.mp3
/usr/local/bin/mpc add http://208.92.53.92:443/CADENADIAL_SC
/usr/local/bin/mpc add http://77.67.34.11:443/LOS40_SC
/usr/local/bin/mpc add http://catradio.ccma.audioemotion.stream.flumotion.com/ccma/catradio.mp3
/usr/local/bin/mpc play

