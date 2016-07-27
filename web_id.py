#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, time
import RPi.GPIO as GPIO
import os
import logging
from gps import *
import threading
import pygame
import pygame.camera
from system_start import get_id, read_pipe

pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

#рівень логування
LOG_LEVEL=logging.DEBUG

#логи в консоль
logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

#підтягнути ID пристрою з файлу

id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)
#print rpi_id
#[4:5]
#звуковий індикатор посвідчень
sig_pin = 18

#логи у файл
logging.basicConfig(filename='/media/usb/logs/web_id.log',format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sig_pin,GPIO.OUT)


#останні коректні координати GPS
latitude_last = ''
longitude_last = ''
#status = 0

#функція запису архівних даних, коли немає доступу до Інтернет
def if_err(filename):
  fn=open('/media/usb/archive/'+filename, 'w')
  fn.write(str(postfor) + "\n" + str(latitude) + "\n" + str(longitude) + "\n" + str('3') + "\n" + str(dayname)+"\n" + str(txtfilename)+"\n")
  fn.close()
  logging.info("create error file: " +txtfilename)

#ініціалізація змінних та функцій для роботи з GPS модулем
gpsd = None
class GpsPoller(threading.Thread):
  def __init__(self):#непонятно для чого тут конструктор?
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
  gpsp = GpsPoller()
  gpsp.start()
#print read_pipe(4,5)
while True:
    time.sleep(0.1)

    
    cam3_state = read_pipe(4, 5)
    
#    try:
#        cam3_state    
#    except BaseException:
#        cam3_state = read_pipe(4, 5)
#        print "this is read_pipe exception!!!"
    print cam3_state

      #якщо натиснута кнопка
    if cam3_state == '0':# and status == 0:

      GPIO.output(sig_pin, GPIO.HIGH)
      time.sleep(0.2)
      GPIO.output(sig_pin, GPIO.LOW)

      #увімкнути світлодіод підсвітки
#      print "LED ON"

      now = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
#      print "hi"
      n = 0
      while n < 2:
        img = cam.get_image()
        jpname = "/media/usb/cam3/"+now+"_"+str(n)
        pygame.image.save(img, jpname+".jpeg")
        n += 1
#      print "after while"

#      logging.info("STOP recording")

      postfor = time.strftime("%Y-%m-%d %H:%M:%S")
      txtfilename = rpi_id+"_"+now+".txt"
      #парсити дату
      dayname=rpi_id+'_'+now[:10]
      daypath='/media/usb/'+rpi_id+'/'+dayname
#      print dayname
#      print daypath
#      print now
#      print rpi_id
      #отримати список файлів(фото)
      #asd = filter(lambda x: x.endswith('.jpg'), files)
      list_files = os.listdir('/media/usb/cam3')
#      print "here"

      f=open(daypath+'/'+rpi_id+'_'+now +'.txt', 'w')
      
#      print "before FOR"

      for index in list_files:
        f.write(index + '\n')
        in_file = '/media/usb/cam3'+'/'+index
        out_file = daypath+'/'+index
        os.rename(in_file, out_file)
        logging.info("moving "+in_file+" to "+out_file)
      f.close()
      #парсити широту і довготу з GPS
      latitude=str(gpsd.fix.latitude)[0:9]
      longitude=str(gpsd.fix.longitude)[0:9]
      
      print latitude

      if latitude != '0' and latitude != 'nan':
        latitude_last = latitude
        longitude_last = longitude
     #якщо координати коректні, запам'ятати їх як останні коректні
      if latitude == 'nan' or latitude == '0.0':
        latitude = latitude_last
        longitude = longitude_last

      #зберегти дані
      if_err(now)
 #     logging.info("filename is: "+filename)
      GPIO.output(sig_pin, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(sig_pin, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(sig_pin, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(sig_pin, GPIO.LOW)
      time.sleep(0.5)

GPIO.output(sig_pin, GPIO.LOW)
GPIO.cleanup()
