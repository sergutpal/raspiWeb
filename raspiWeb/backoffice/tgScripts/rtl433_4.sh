#!/bin/bash
/usr/local/bin/rtl_433 -F json -M utc -R 48 | mosquitto_pub -h 192.168.1.20 -p 1883 -u sergutpal -P SGp24121976 -t RTL433/cmd -l
