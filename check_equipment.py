# -*- coding: utf-8 -*-
import os
from gps import *
import time
import threading
import requests
import re
import datetime
import RPi.GPIO as GPIO
import logging
import urllib2
import commands
from shiftr_74HC595.shiftr_74HC595 import ShifRegister
from system_start import get_id

#рівень логування
LOG_LEVEL=logging.DEBUG

#логи в консоль
logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

data_pin = 7 #pin 14 on the 75HC595
latch_pin = 5 #pin 12 on the 75HC595
clock_pin = 3 #pin 11 on the 75HC595
shift_register = ShifRegister(data_pin, latch_pin, clock_pin) #using the class to manage the shift register

count = 0

#path = "/home/pi/taxi/my_program.fifo"
#підтягнути ID пристрою

id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)

logging.debug("RPi ID = "+rpi_id)

def internet_on(ip_adress):
    try:
      urllib2.urlopen(ip_adress, timeout=10)
      return True
    except urllib2.URLError:
        pass
    return False

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
        #парсити широту, довготу, час і швидкість з GPS
        latitude = str(gpsd.fix.latitude)[:9]
	#якщо координати коректні
        if latitude != '0.0' and latitude != 'nan':
        #засвітити світлодіодний індикатор
          shift_register.setOutput(4, GPIO.LOW)
      #інакше погасити світлодіодний індикатор
        elif latitude == '0.0' or latitude == 'nan':
          shift_register.setOutput(4, GPIO.HIGH)
        if internet_on('http://google.com.ua/'):
          shift_register.setOutput(3, GPIO.LOW)
          count = 0
        else:
          output = commands.getoutput('ps -A')
          shift_register.setOutput(3, GPIO.HIGH)
          if not output.find('pppd'):
            if os.path.exists('/dev/ttyACM0'):
              os.system('sudo pppd call mtsconnect &')
            else:
              os.system('sudo pppd call mts &')
          count += 1
#          print count
          if count >= 80:
            os.system('sudo killall pppd')
            count = 0
        cam1_ip = '192.168.1.11'
        cam1_resp = os.system("ping -c 1 -W 1 " + cam1_ip)
        if not cam1_resp:
          shift_register.setOutput(5, GPIO.LOW)
        else:
          shift_register.setOutput(5, GPIO.HIGH)
        cam2_ip = '192.168.1.12'
        cam2_resp = os.system("ping -c 1 -W 1 " + cam2_ip)
        if not cam2_resp:
          shift_register.setOutput(6, GPIO.LOW)
        else:
          shift_register.setOutput(6, GPIO.HIGH)

        shift_register.setOutput(0, GPIO.HIGH)
        shift_register.setOutput(1, GPIO.HIGH)
        shift_register.setOutput(2, GPIO.HIGH)
        shift_register.setOutput(7, GPIO.HIGH)

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing

#perevireno
