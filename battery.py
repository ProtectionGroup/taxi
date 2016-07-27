# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import os
import logging
import time
import requests
import datetime
from system_start import get_id, read_pipe

#рівень відладки для логування
LOG_LEVEL=logging.DEBUG

#логи в консоль
logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

#логи у файл
logging.basicConfig(filename='/media/usb/logs/battery.log',format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

path = "/home/pi/taxi/my_program.fifo"# перевірка на шлях
try:
  os.path.exists(path)
except OSError:
  os.makedirs(path)
#підтягнути ID пристрою з файлу
#id_bin = get_id()
#print id_bin


id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)
print rpi_id



#def read_pipe(pipe_path):
#    fifo = open(pipe_path, "r")
#    line_stack = ''
#    for line in fifo:#????
#      line_stack = line[7:8]
#    fifo.close()
#    return line_stack

#адреса для відправки POST-запитів
adr = "http://bus.or-za.com/device/controller/"+rpi_id

while True:
    time.sleep(2)
    pow_state = read_pipe(7,8)
    if len(pow_state) > 0:
      print pow_state
      pass
    else:
      continue
    if pow_state == '0':
        logging.info("powering from baterry"+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
          #формувати запит
        payload = {
          'time_gps': datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
          'latitude': ' ',
          'longitude': ' ',
          'type': ' ',
          'speed': ' ',
          'fold_name': ' ',
          'file_name': ' ',
          'endtime': ' ',
          'power': 'poweroff',
          'system_timer': ' '
        }
        r = requests.post(adr, timeout=20, data=payload)
        logging.debug("POST: " +str(payload))
        logging.info("SYSTEM IS GOING DOWN!!!"+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')))
        os.system("sudo shutdown -h now")

GPIO.cleanup()
#Перевірено
