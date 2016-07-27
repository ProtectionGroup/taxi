import calendar
import requests
import time
import datetime
import urllib2
import os
import logging
from system_start import get_id

LOG_LEVEL=logging.DEBUG
logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

#path = "/home/pi/taxi/my_program.fifo"

rpi_id = str(int(get_id(),2))
logging.debug("RPi ID = "+rpi_id)

def internet_on(ip_adress):
    try:
      response=urllib2.urlopen(ip_adress,timeout=10)
      return True
    except urllib2.URLError as err: pass
    return False

adr="http://glob-control.com/"+rpi_id+".html"
system_timer = 0

while True:

    if system_timer == 0:
      if internet_on('http://google.com.ua/'):
        os.system("sudo sntp -s 0.ua.pool.ntp.org > /dev/null &")
        time.sleep(2)
      for_post = time.strftime("%Y-%m-%d %H:%M:%S")
      start = calendar.timegm(time.gmtime())
      payload = {'time_gps': for_post, 'latitude': ' ', 'longitude': ' ', 'type': ' ', 'speed': ' ', 'fold_name': ' ', 'file_name': ' ', 'endtime': ' ', 'power': ' ', 'system_timer': system_timer}
      logging.debug("POST: " +str(payload))
      try:
        r = requests.post(adr, timeout=10, data=payload)
      except:
        pass
    start = calendar.timegm(time.gmtime())
    not_end = True
    while (not_end):
      time.sleep(1)
      system_timer += 1
      end = calendar.timegm(time.gmtime())
      res = end - start
      if res >= 300:
        next_for_post = time.strftime("%Y-%m-%d %H:%M:%S")
        payload = {'time_gps': next_for_post, 'latitude': ' ', 'longitude': ' ', 'type': ' ', 'speed': ' ', 'fold_name': ' ', 'file_name': ' ', 'endtime': ' ', 'power': ' ', 'system_timer': system_timer}
        logging.debug("POST: " +str(payload))
        try:
          r = requests.post(adr, timeout=10, data=payload)
          not_end = False
        except:
          pass
