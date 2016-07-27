
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

comlogs = "sudo cp /tmp/*.log /media/usb/logs/"
os.system(comlogs)

if not output.find('wput'):
    os.system("cd /media/usb/logs && sudo /usr/bin/wput -B '.' ftp://busftp:toW8obfwoPFtLq@5.58.14.177/web/bus_video/"+rpi_id+"/logs/")
