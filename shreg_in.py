#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import os
#import threading

#lock = threading.Lock()
#id_path = "/home/pi/taxi/my_program.fifo"
#if not os.path.exists(id_path):#може бути помилка якщо шлях не повний os.makedirs()
#  os.mkfifo(id_path)

os.system("/usr/bin/python /home/pi/taxi/system_start.py > /dev/null &")

ParallelLoadPin = 33
ClockPin = 35
DataPin = 31
valuers = range(25)

def set_gpio():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(ParallelLoadPin,GPIO.OUT)
  GPIO.output(ParallelLoadPin, GPIO.HIGH)
  GPIO.setup(ClockPin,GPIO.OUT)
  GPIO.output(ClockPin, GPIO.HIGH)
  GPIO.setup(DataPin,GPIO.IN)

def par_dat():
  GPIO.output(ParallelLoadPin, GPIO.HIGH)
  time.sleep(0.0001)
  GPIO.output(ParallelLoadPin, GPIO.LOW)
  time.sleep(0.0001)
  GPIO.output(ParallelLoadPin, GPIO.HIGH)
  time.sleep(0.0001)

def clock_165():
  GPIO.output(ClockPin, GPIO.HIGH)
  time.sleep(0.0001)
  GPIO.output(ClockPin, GPIO.LOW)
  time.sleep(0.0001)
  GPIO.output(ClockPin, GPIO.HIGH)
  time.sleep(0.0001)

#def read_pipe(start, end):
#  fifo = open("/home/pi/taxi/my_program.fifo", "r")
#  for i in fifo:
#    line = i[start:end]
#  fifo.close()
  #print line
#  return line



while True:
  set_gpio()
  GPIO.output(ClockPin, GPIO.LOW)
  time.sleep(0.0001)
  par_dat()
  my_arr = ''
  for i in range(25):
    clock_165()
    valuers[24-i] = GPIO.input(DataPin)
  cam1 = valuers[3]
  my_arr = str(cam1)
  cam2 = valuers[4]
  my_arr = str(cam2)
  butt = valuers[5]
  my_arr = str(butt)
  E3 = valuers[6]
  my_arr = str(E3)
  E4 = valuers[7]
  my_arr = str(E3)
  E5 = valuers[8]
  E6 = valuers[9]
  E7 = valuers[10]
  id_0 = valuers[19]
  id_0 = 1 - id_0 #-=1
  id_1 = valuers[20]
  id_1 = 1 - id_1
  id_2 = valuers[21]
  id_2 = 1 - id_2
  id_3 = valuers[22]
  id_3 = 1 - id_3
  id_4 = valuers[15]
  id_4 = 1 - id_4
  id_5 = valuers[16]
  id_5 = 1 - id_5
  id_6 = valuers[17]
  id_6 = 1 - id_6
  id_7 = valuers[18]
  id_7 = 1 - id_7
  id_8 = valuers[12]
  id_8 = 1 - id_8
  id_9 = valuers[11]
  id_9 = 1 - id_9
  id_A = valuers[13]
  id_A = 1 - id_A
  id_B = valuers[14]
  id_B = 1 - id_B
  id_C = valuers[23]
  my_arr = str(cam1)+str(cam2)+str(butt)+str(E3)+str(E4)+str(E5)+str(E6)+str(E7)+str(id_B)+str(id_A)+str(id_9)+str(id_8)+str(id_7)+str(id_6)+str(id_5)+str(id_4)+str(id_3)+str(id_2)+str(id_1)+str(id_0)
  print my_arr

#  lock.acquire()

  id_path = "/home/pi/taxi/my_program.fifo"
  if not os.path.exists(id_path):#може бути помилка якщо шлях не повний os.makedirs()
      os.mkfifo(id_path)  
  fifo = open(id_path, "w")
  fifo.write(my_arr)
  fifo.close()
#  lock.release()
   #os.system("/usr/bin/python /home/pi/taxi/system_start.py > /dev/null &")
  if KeyboardInterrupt:
      GPIO.cleanup()
#перевірено
