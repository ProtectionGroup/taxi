import commands
import os
from system_start import get_id

id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)

output = commands.getoutput('ps -A')
#print "1"
if 'wput' not in output:
    os.system("cd /media/usb/ && sudo /usr/bin/wput -B -u -R -a /media/usb/logs/wput.log "+rpi_id+" ftp://busftp:toW8obfwoPFtLq@5.58.14.177/web/bus_video/")
#    print "2"
