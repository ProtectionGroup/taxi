# -*- coding: utf-8 -*-
import os, sys
#from battery import get_id
from gps import *
import time
import threading
import requests
import re
import datetime
import RPi.GPIO as GPIO
import logging
from system_start import get_id
#import commands

#coordinates_path = "/home/pi/taxi/counters/coordinates.fifo"
#if os.path.exists(coordinates_path):
#  pass
#else:
#  os.mkfifo(coordinates_path)

#рівень логування
LOG_LEVEL=logging.DEBUG

#логи в консоль
logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

#логи у файл
logging.basicConfig(filename='/media/usb/logs/post_gps.log',format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

type = 5

#path = "/home/pi/taxi/my_program.fifo"
#підтягнути ID пристрою

id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)

logging.info("RPi ID = "+rpi_id)

#адреса для відправки POST-запитів
adr="http://bus.or-za.com/device/controller/"+rpi_id

#функція запису архівних даних, коли немає доступу до Інтернет
def if_err(name):
  fn=open('/media/usb/archive_gps/'+name, 'w')
  fn.write(str(time_gps) + "\n" + str(latitude) + "\n" + str(longitude) + "\n" + str(speed) + "\n" + str(type)+"\n")
  fn.write("\n")
  fn.write("\n")
  fn.close()


#ініціалізація змінних та функцій для роботи з GPS модулем
gpsd = None
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start()

#цикл
    while True:
      time.sleep(1)
      try:
          #парсити дату
        now=datetime.datetime.now().strftime('%Y-%m-%d')#datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dayname=rpi_id+'_'+now#now[10]
        name=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        logging.info("START TIME: "+ str(name))#+str(now)
        txt=rpi_id+'_'+name+'.txt'

        #парсити широту, довготу, час і швидкість з GPS
        latitude=str(gpsd.fix.latitude)[:9]
        #latitude=latitude[0:9]
        logging.debug("latitude: " +latitude)
        longitude=str(gpsd.fix.longitude)[:9]
        #longitude=longitude[0:9]
        logging.debug("longitude: " +longitude)

        time_gps = time.strftime("%Y-%m-%d %H:%M:%S")

        #logging.debug("time: " +str(time_gps))

        speed = gpsd.fix.speed
        #logging.debug("speed: " +str(speed))

      #якщо координати коректні
        if latitude!='0.0' and latitude!='nan' and longitude!='0.0' and longitude!='nan':
 #         coordinates = latitude + '\n' + longitude
 #         fifo = open("/home/pi/taxi/counters/coordinates.fifo", "w")
 #         fifo.write(coordinates)
 #         fifo.close()
          logging.debug("LED on")

       #формувати POST-запит
          payload = {
            'time_gps': time_gps,
            'latitude': latitude,
            'longitude': longitude,
            'type': '4',
            'speed': speed,
            'fold_name': ' ',
            'file_name': ' '
          }
          logging.debug("POST: " +str(payload))
          try:
          #надіслати запит
            requests.post(adr, timeout=10, data=payload)
       #якщо помилка, отримати код і записати дані в архів
          except requests.exceptions.RequestException:
            if_err(name)
            time.sleep(4)
      #інакше погасити світлодіодний індикатор

        if latitude == '0.0' or latitude == 'nan' or longitude == '0.0' or longitude == 'nan' or speed == 'nan':
          print "LED OFF"

    #якщо каталог з архівними записами не пустий

        list_of_dirs = os.listdir('/media/usb/archive_gps/')#list reserved name
        if len(list_of_dirs) != 0:#перевірити наявність файлів у папці, бібліотека os
      #відкрити перший архівний файл
          f=open('/media/usb/archive_gps/'+list_of_dirs[0], 'r')
      #зчитати перший архівний файл
          l=f.readlines()
          f.close()
        #парсити перший архівний файл               #try...except, strip
          if len(l) > 1:
            payload2 = {}
            time_a = l[0]
            payload2['time_gps'] = re.sub("^\s+|\n|\r|\s+$", '', time_a)
            latitude_a = l[1]
            payload2['latitude'] = re.sub("^\s+|\n|\r|\s+$", '', latitude_a)
            longitude_a = l[2]
            payload2['longitude'] = re.sub("^\s+|\n|\r|\s+$", '', longitude_a)
            speed_a = l[3]
            payload2['speed'] = re.sub("^\s+|\n|\r|\s+$", '', speed_a)
            type_a = l[4]
            payload2['type'] = re.sub("^\s+|\n|\r|\s+$", '', type_a)
            dayname_a = l[5]
            payload2['fold_name'] = re.sub("^\s+|\n|\r|\s+$", '', dayname_a)
            filename_a = l[6]
            payload2['file_name'] = re.sub("^\s+|\n|\r|\s+$", '', filename_a)
          #формувати запит з даними архівного файлу
            """
            payload2 = {'time_gps': time_a, 'latitude': latitude_a, 'longitude': longitude_a, 'type': type_a, 'speed': speed_a, 'fold_name': ' ', 'file_name': ' '}
            """
        #надіслати POST з архівними даними
            try:
              requests.post(adr, timeout=10, data=payload2)
              #видалити перший архівний файл, якщо надіслано
              os.system("sudo rm /media/usb/archive_gps/"+list_of_dirs[0])
            except:
              pass
          else:
            os.system("sudo rm /media/usb/archive_gps/"+list_of_dirs[0])
        #парсити дату
        dayname=rpi_id+'_'+datetime.datetime.now().strftime('%Y-%m-%d')

      #перевірити існування/створити директорію з поточною датою
        daypath='/media/usb/'+rpi_id+'/'+dayname
        if not os.path.exists(daypath):
          os.makedirs(daypath)

      except:
        pass

#      if latitude != 'nan' and latitude != '0.0' and longitude != 'nan' and longitude != '0.0':
#        coordinates = latitude + '\n' + longitude
#        fifo = open("/home/pi/taxi/counters/coordinates.fifo", "w")
#        fifo.write(coordinates)
#        fifo.close()

  except (KeyboardInterrupt, SystemExit):
    gpsp.running = False
    gpsp.join()
