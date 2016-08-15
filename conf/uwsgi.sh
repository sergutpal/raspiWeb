#!/bin/bash

#exec /usr/local/bin/uwsgi --emperor /etc/uwsgi/sites --daemonize /home/nfs/raspiWeb/logs/uwsgi.log
exec /usr/local/bin/uwsgi --ini /etc/uwsgi/sites/raspiWeb.ini

