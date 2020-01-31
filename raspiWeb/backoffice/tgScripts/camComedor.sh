NOW=$(date +"%d%m%Y_%H%M%S")
ffmpeg -i rtsp://admin:KVHPVD@192.168.1.224:554  -c copy -r 5 -t 60 /home/tmp/camComedor/$NOW.mp4
sleep 1
mv /home/tmp/camComedor/$NOW.mp4 /home/tmp/dropbox/camComedor
