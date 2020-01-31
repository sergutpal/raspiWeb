NOW=$(date +"%d%m%Y_%H%M%S")
ffmpeg -i rtsp://admin:VTLOZG@192.168.1.220:554 -c copy -r 5 -t 60 /home/tmp/camEntrada/$NOW.mp4
sleep 1
mv /home/tmp/camEntrada/$NOW.mp4 /home/tmp/dropbox/camEntrada
