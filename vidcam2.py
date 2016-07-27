#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, time
import RPi.GPIO as GPIO
import os
import subprocess, signal
import logging
from gps import *
import threading
from system_start import get_id, read_pipe

#рівень логування
LOG_LEVEL=logging.DEBUG

#логи в консоль
logging.basicConfig(format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')

#path = "/home/pi/taxi/my_program.fifo"
#підтягнути ID пристрою з файлу

id_bin = get_id()

try:
    id_int = int(id_bin, 2)
except BaseException:
    id_bin = get_id()
    id_int = int(id_bin, 2)

rpi_id = str(id_int)
logging.debug("RPi ID = "+rpi_id)

#адреса для відправки POST-запитів
adr="http://glob-control.com/"+rpi_id+".html"

#логи у файл
#logging.basicConfig(filename='/media/usb/logs/vidcam2.log',format='%(levelname)s[%(asctime)s] %(message)s',level=LOG_LEVEL, datefmt='%m/%d/%Y %I:%M%p')


#функція запису архівних даних, коли немає доступу до Інтернет
def if_err(filename):
  fn=open('/media/usb/archive/'+filename, 'w')
  fn.write(str(postfor) + "\n" + str(latitude) + "\n" + str(longitude) + "\n" + str("2") + "\n" + str(dayname)+"\n" + str(filename)+"\n" + str(date_now)+"\n")
  fn.close()
  logging.info("create error file: " +filename)

#[2:3]
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
  gpsp = GpsPoller()
  gpsp.start()

#останні коректні координати GPS
latitude_last = ''
longitude_last = ''
speed_last = ''

while True:
  time.sleep(1)

  cam1_state = read_pipe(2, 3)
  print cam1_state

  #якщо двері відкрито
  if cam1_state=='1':

    now = time.strftime("%Y-%m-%d_%H-%M-%S")

    postfor = time.strftime("%Y-%m-%d %H:%M:%S")
    filename = str(now)+"--2"
    logging.info("datetime = "+now)
    pro = subprocess.Popen(["/usr/bin/mplayer", "-dumpstream", "http://admin:admin@192.168.1.12/video/mjpg.cgi", "-dumpfile", "/media/usb/cam2/"+filename+".mjpeg"], preexec_fn=os.setsid)
    start_time=calendar.timegm(time.gmtime())
    logging.info("START TIME = "+str(start_time))
    logging.info("START recording...")
    not_end = True
    while (not_end):
      time.sleep(1)
      end_time=calendar.timegm(time.gmtime())
      delay=end_time-start_time

      #якщо двері закрилися

      
      cam1_state = read_pipe(2, 3)
      print cam1_state

      if cam1_state == '0':
        time.sleep(4)

        cam1_state = read_pipe(2, 3)
        print cam1_state

        if cam1_state == '0':
          not_end = False
          logging.info("STOP recording")
        else:
          pass

      if delay >= 1800:
        not_end = False
        logging.info("STOP recording after 30 min")

    #припинити зйомку
    os.killpg(pro.pid, signal.SIGINT)

    logging.info("pid = "+str(pro.pid)+" WAS KILLED")

    #парсити дату
    date_now=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    dayname=rpi_id+'_'+date_now[:10]
    logging.info("getting name for dayname folder: "+ str(dayname))
    logging.info("getting date: "+ str(date_now))

    #парсити широту і довготу з GPS
    latitude=str(gpsd.fix.latitude)[0:9]
    longitude=str(gpsd.fix.longitude)[0:9]
    if latitude != '0.0' and latitude != 'nan':
      latitude_last = latitude
      longitude_last = longitude

   #якщо координати коректні, запам'ятати їх як останні коректні
    if latitude == 'nan' or latitude == '0.0':
      latitude=latitude_last
      longitude=longitude_last

    #зберегти дані
    if_err(filename)
    logging.info("filename is: "+filename)

    try:
      os.rename("/media/usb/cam2/"+filename+".mjpeg", '/media/usb/'+rpi_id+'/'+dayname+'/'+filename+".mjpeg")
    except:
      continue
  if KeyboardInterrupt:
    GPIO.cleanup()
