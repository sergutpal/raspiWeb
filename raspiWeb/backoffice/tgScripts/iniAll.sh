#!/bin/bash

now=$(date +"%d/%m/%Y %H:%M:%S")
host=$(</etc/hostname)
iniFile="/home/tmp/telegram/logs/ini$host.log"
echo $host '-' $now Inicializada >> $iniFile
exit 0
