MSG="Chicos, han llamado a la puerta. Repito, han llamado a la puerta. Por favor, no quiero ser pesada, pero han llamado a la puerta"
VOL=70
#/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" ALL $VOL

/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" DotSalon $VOL
sleep 1
/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" DotDormitorio $VOL
sleep 1
/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" DotDespacho $VOL
sleep 1
/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" ShowPeques $VOL
sleep 1
/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" ShowCocina $VOL
