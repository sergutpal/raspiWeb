MSG="ALARMA, ALEXA HA DETECTADO UNA INTRUSIÓN EN CASA. ALARMA, ALEXA HA DETECTADO UNA INTRUSIÓN EN CASA. ALARMA, ALEXA HA DETECTADO UNA INTRUSIÓN EN CASA. Aquellos que hayáis entrado en esta casa debéis saber que hay un total de 7 cámaras, 2 exteriores y 5 en diferentes zonas de la casa y que se está grabando todo y subiéndolo en tiempo real a Amazon Cloud Drive. También debéis saber que acabo de avisar al propietario de la casa para que se ponga en contacto de forma inmediata con la policía y que presente como prueba las imágenes que se están grabando en todo este tiempo."
VOL=100
#/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" ALL $VOL

/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" DotSalon $VOL
sleep 1
#/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" DotDormitorio $VOL   # En el dormitorio queremos que suene el altavoz normal via bluetooth
#sleep 1
/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" DotDespacho $VOL
sleep 1
/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" ShowPeques $VOL
sleep 1
/home/nfs/telegram/tgScripts/alexaTTS/alexatts.sh "$MSG" ShowCocina $VOL
