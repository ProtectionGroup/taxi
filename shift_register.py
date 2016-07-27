import RPi.GPIO as GPIO
from shiftr_74HC595.shiftr_74HC595 import ShifRegister #importing the downloaded class
from time import sleep

GPIO.setmode(GPIO.BOARD)

data_pin = 7 #pin 14 on the 75HC595
latch_pin = 5 #pin 12 on the 75HC595
clock_pin = 3 #pin 11 on the 75HC595
shift_register = ShifRegister(data_pin, latch_pin, clock_pin) #using the class to manage the shift register

try:
    while 1:
        #setting the pins to turn on or off the leds
        for i in range(7):
            shift_register.setOutput(i, GPIO.HIGH)
            """
        shift_register.setOutput(0, GPIO.HIGH)
        shift_register.setOutput(1, GPIO.HIGH)
        shift_register.setOutput(2, GPIO.HIGH)
        shift_register.setOutput(3, GPIO.HIGH)
        shift_register.setOutput(4, GPIO.HIGH)
        shift_register.setOutput(5, GPIO.HIGH)
        shift_register.setOutput(6, GPIO.HIGH)
        """
        shift_register.setOutput(7, GPIO.LOW)
        sleep(.1)

        #setting the pins to turn on or off the leds
        for i in range(7):
            shift_register.setOutput(i, GPIO.LOW)
            """
        shift_register.setOutput(0, GPIO.LOW)
        shift_register.setOutput(1, GPIO.LOW)
        shift_register.setOutput(2, GPIO.LOW)
        shift_register.setOutput(3, GPIO.LOW)
        shift_register.setOutput(4, GPIO.LOW)
        shift_register.setOutput(5, GPIO.LOW)
        shift_register.setOutput(6, GPIO.LOW)
        """
        shift_register.setOutput(7, GPIO.HIGH)
        sleep(.1)
except KeyboardInterrupt:
    print "Ctrl-C - quit"

GPIO.cleanup() #cleaning all the GPIO pins when the script is finished
