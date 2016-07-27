#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import RPi.GPIO as GPIO
import os
#import subprocess, signal
import logging
from gps import *
import threading

import pygame
import pygame.camera

#counter_path = "/home/pi/taxi/counters/web_id.fifo"
#if os.path.exists(counter_path):
#  pass
#else:
#  os.mkfifo(counter_path)


pygame.camera.init()
#pygame.camera.list_camera() #Camera detected or not
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

#рівень логування
LOG_LEVEL=logging.DEBUG

#логи в консоль
#logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

path = "/home/pi/taxi/my_program.fifo"
counter_fifo = 0

#підтягнути ID пристрою з файлу
def get_id():
  fifo = open(path, "r")
  for id in fifo:
    line_id = id[8:20]
  fifo.close()
  line_id = int(line_id, 2)

  return line_id

id =  get_id()
print id
rpi_id = id
rpi_id = str(rpi_id)

def read_pipe():
  fifo = open(path, "r")
  for line in fifo:
    line = line[4:5]
  fifo.close()
  return line

#звуковий індикатор посвідчень
sig_pin = 18

#логи у файл
logging.basicConfig(filename='/media/usb/logs/web_id.log',format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sig_pin,GPIO.OUT)


#останні коректні координати GPS
latitude_last = ''
longitude_last = ''
speed_last = ''

#функція запису архівних даних, коли немає доступу до Інтернет
def if_err(filename):
  fn=open('/media/usb/archive/'+filename, 'w')
  fn.write(str(postfor) + "\n")
  fn.write(str(latitude) + "\n")
  fn.write(str(longitude) + "\n")
  fn.write(str(speed) + "\n")
  fn.write(str("3") + "\n")
  fn.write(str(dayname)+"\n")
  fn.write(str(txtfilename)+"\n")
  fn.close()
  #logging.info("create error file: " +txtfilename)

try:
  while True:
    time.sleep(0.1)

    try:
      cam3_state = read_pipe()
    except:
      continue
    print cam3_state
      #якщо натиснута кнопка
    if cam3_state=='0':
      GPIO.output(sig_pin, GPIO.HIGH)
      time.sleep(0.2)
      GPIO.output(sig_pin, GPIO.LOW)
      #увімкнути світлодіод підсвітки
      now = time.strftime("%Y-%m-%d_%H-%M-%S")
      filename = str(now)
  #    logging.info("datetime = "+now)
      n = 0
      while n < 2:
        img = cam.get_image()
        jpname = "/media/usb/cam3/"+filename+"_"+str(n)
        pygame.image.save(img, jpname+".jpeg")
      #  img = None
        n = n + 1
      #logging.info("STOP recording")

      #logging.info("pid = "+str(pro.pid)+" WAS KILLED")

      now = time.strftime("%Y-%m-%d_%H-%M-%S")
      postfor = time.strftime("%Y-%m-%d %H:%M:%S")
      filename = str(now)
      txtfilename = rpi_id+"_"+filename+".txt"
      #парсити дату
      date_now=datetime.datetime.now().strftime('%Y-%m-%d')
      dayname=rpi_id+'_'+date_now
 #     logging.info("getting name for dayname folder: "+ str(dayname))
      dname=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  #    logging.info("getting date: "+ str(dname))

      daypath='/media/usb/'+rpi_id+'/'+dayname

      #отримати список файлів(фото) 
      directory = '/media/usb/cam3'
      list = os.listdir(directory)
      txtname=daypath+'/'+rpi_id+'_'+filename +'.txt'
      f=open(txtname, 'w')
      count=0
      for index in list:
        f.write(index + '\n')
        in_file = directory+'/'+index
        out_file = daypath+'/'+index 
        os.rename(in_file, out_file)
       # logging.info("moving "+in_file+" to "+out_file)
        count+=1
      f.close()
      photo_counter = count
      logging.info("file named " + txtname +" was created: "+str(count) + " files")

      #парсити широту і довготу з GPS









 #     logging.debug("latitude = " + str(latitude) + " longitude = " + str(longitude)+ "speed = "+ str(speed))

     #якщо координати коректні, запам'ятати їх як останні коректні
      if latitude=='nan' or latitude=='0.0':
        latitude=latitude_last
 
      if  longitude=='0.0' or longitude=='nan':
        longitude=longitude_last
     
      if  speed == 'nan':
        speed=speed_last

      #зберегти дані
      if_err(filename)
 #     logging.info("filename is: "+filename)

      not_end = True
      while (not_end):
        time.sleep(0.3)
        try:
          cam3_state = read_pipe()
        except:
          continue
        #якщо кнопка відтиснута
        if cam3_state=='1':
          not_end = False

      GPIO.output(sig_pin, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(sig_pin, GPIO.LOW)
      time.sleep(0.1)
      GPIO.output(sig_pin, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(sig_pin, GPIO.LOW)

      counter_fifo = counter_fifo + 1
      fifo = open(counter_path, "w")
      fifo.write(counter_fifo)
      fifo.close()
except:
  GPIO.output(sig_pin, GPIO.LOW)
  GPIO.cleanup()

