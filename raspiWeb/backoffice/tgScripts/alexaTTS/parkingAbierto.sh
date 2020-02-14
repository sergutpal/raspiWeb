MSG="Chicos, la puerta del parking está abierta. Repito, la puerta del parking lleva un buen rato abierta. Por favor, revisad la puerta del parking"
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
