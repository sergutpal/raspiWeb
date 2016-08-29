#!/bin/bash

/usr/local/bin/mpc clear
#/usr/local/bin/mpc ls | /usr/local/bin/mpc add
/usr/local/bin/mpc add http://listen.radionomy.com:80/1HITS80s
/usr/local/bin/mpc add http://91.121.68.52:8012/
/usr/local/bin/mpc add http://212.129.60.86:9948
/usr/local/bin/mpc add http://84.127.246.10:8085
/usr/local/bin/mpc add http://188.93.73.98:8114
#/usr/local/bin/mpc add http://195.10.10.222/cope/rockfm.mp3
/usr/local/bin/mpc play
