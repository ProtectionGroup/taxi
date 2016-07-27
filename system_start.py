# -*- coding: utf-8 -*-
import os
import datetime


#sys_path = "/home/pi/taxi/my_program.fifo"
if not os.path.exists("/home/pi/taxi/my_program.fifo"):
  os.mkfifo("/home/pi/taxi/my_program.fifo")

# підтягнути ID пристрою
def get_id():
  fifo = open("/home/pi/taxi/my_program.fifo")
  da = fifo.read().strip()
  if len(da)>0:
      pull_id = da[8:20]
      fifo.close()
      return pull_id
  else:
      fifo.close()
      get_id()

def read_pipe(start, end):
  fifo = open("/home/pi/taxi/my_program.fifo", "r")
  rda = fifo.read().strip()
  if len(rda)>0:
      pull_id = rda[start:end]
      fifo.close()
      return pull_id
  else:
      fifo.close()
      read_pipe(start, end)

id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)

#print rpi_id

dayname = rpi_id + '_' + datetime.datetime.now().strftime('%Y-%m-%d')
# перевірити існування/створити директорію з поточною датою
daypath = '/media/usb/' + rpi_id + '/' + dayname

list_dirs = [
  '/media/usb/logs',
  '/media/usb/archive_gps',
  '/media/usb/cam1',
  '/media/usb/cam2',
  '/media/usb/archive',
  '/media/usb/archive_gps',
  '/media/usb/cam3'
  ]
list_dirs.append('/media/usb/' + rpi_id)
list_dirs.append('/media/usb/' + rpi_id + '/' + dayname)
for ex_path in list_dirs:
  try:
      os.makedirs(ex_path)
  except OSError:
      continue
#print 'Hi'
