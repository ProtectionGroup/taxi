#!/bin/bash
cd /home/pi/taxi

sudo python /home/pi/taxi/check_ftp.py > /dev/null &

exit 0
