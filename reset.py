import os, sys
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

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

out_con_Pin = 12
GPIO.setup(out_con_Pin, GPIO.OUT)
state = 1

while True:
  GPIO.output(out_con_Pin, state)
  state = 1 - state
  time.sleep(1)
#  print "OK"
