# -*- coding: utf-8 -*-
import requests
import re
import os
import logging
import time
import datetime
from system_start import get_id

#рівень логування
#LOG_LEVEL=logging.DEBUG

#логи в консоль
logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M%p')
"""
logging.basicConfig(filename='/media/usb/logs/send_test.log',format='%(levelname)s[%(asctime)s] %(message)s',level=logging.DEBUG,datefmt='%m/%d/%Y %I:%M%p')
"""
#path = "/home/pi/taxi/my_program.fifo"
#підтягнути ID пристрою з файлу

id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)

logging.info("id = "+rpi_id)

#останні коректні координати GPS
latitude_last = ''
longitude_last = ''

#адреса для відправки POST-запитів
adr="http://bus.or-za.com/device/controller/"+rpi_id
cont_sum_new = 0

while True:
  time.sleep(3)

  #якщо каталог з архівними записами не пустий
  list_dirs=os.listdir('/media/usb/archive/')

  if len(list_dirs) != 0:

    #відкрити перший архівний файл
    f=open('/media/usb/archive/'+list_dirs[0], 'r')

    #зчитати перший архівний файл
    l=f.readlines()
    f.close()

    #парсити перший архівний файл
    if len(l) == 7:

      time_a = l[0]
      time_a = re.sub("^\s+|\n|\r|\s+$", '', time_a)
      latitude_a = l[1]
      latitude_a = re.sub("^\s+|\n|\r|\s+$", '', latitude_a)
      longitude_a = l[2]
      longitude_a = re.sub("^\s+|\n|\r|\s+$", '', longitude_a)
      type_a = l[3]
      type_a = re.sub("^\s+|\n|\r|\s+$", '', type_a)
      dayname_a = l[4]
      dayname_a = re.sub("^\s+|\n|\r|\s+$", '', dayname_a)
      filename_a = l[5]
      filename_a = re.sub("^\s+|\n|\r|\s+$", '', filename_a)
      endtime = l[6]
      endtime = re.sub("^\s+|\n|\r|\s+$", '', endtime)
      dayname=rpi_id+'_'+datetime.datetime.now().strftime('%Y-%m-%d')
      daypath='/media/usb/'+rpi_id+'/'+dayname+'/'+list_dirs[0]+'.mjpeg'
      if os.path.exists(daypath):
        if type_a == '1' or type_a == '2':
          cont_sum = os.popen("md5sum "+daypath).read()[:32]
          #cont_sum_new = cont_sum[0:32]

      #формувати запит з даними архівного файлу
      payload2 = {'time_gps': time_a, 'latitude': latitude_a, 'longitude': longitude_a, 'type': type_a, 'speed': cont_sum_new, 'fold_name': dayname_a, 'file_name': filename_a, 'endtime': endtime}
      logging.debug("POST: " +str(payload2))

      #надіслати POST з архівними даними
      try:
        r2 = requests.post(adr, timeout=10, data=payload2)
        #видалити перший архівний файл, якщо надіслано
        os.remove("/media/usb/archive/"+list_dirs[0])
      except requests.exceptions.RequestException:
        pass

    if len(l) == 6:
      time_a = l[0]
      time_a = re.sub("^\s+|\n|\r|\s+$", '', time_a)
      latitude_a = l[1]
      latitude_a = re.sub("^\s+|\n|\r|\s+$", '', latitude_a)
      longitude_a = l[2]
      longitude_a = re.sub("^\s+|\n|\r|\s+$", '', longitude_a)
      type_a = l[3]
      type_a = re.sub("^\s+|\n|\r|\s+$", '', type_a)
      dayname_a = l[4]
      dayname_a = re.sub("^\s+|\n|\r|\s+$", '', dayname_a)
      filename_a = l[5]
      filename_a = re.sub("^\s+|\n|\r|\s+$", '', filename_a)

      #формувати запит з даними архівного файлу
      payload2 = {'time_gps': time_a, 'latitude': latitude_a, 'longitude': longitude_a, 'type': type_a, 'speed': '0', 'fold_name': dayname_a, 'file_name': filename_a}
      logging.debug("POST: " +str(payload2))

      #надіслати POST з архівними даними
      try:
        r2 = requests.post(adr, timeout=10, data=payload2)

        #видалити перший архівний файл, якщо надіслано
        os.remove("/media/usb/archive/"+list_dirs[0])
      except requests.exceptions.RequestException:
        pass
    elif len(l) < 3:
        os.remove("/media/usb/archive/"+list_dirs[0])
