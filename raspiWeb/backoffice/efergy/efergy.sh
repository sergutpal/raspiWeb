#!/bin/bash
/usr/local/bin/rtl_fm -f 433505000 -s 200000 -r 96000 -A fast -p 60 -g 49.6 2>/dev/null | /home/nfs/raspiWeb/raspiWeb/backoffice/efergy/efergy
