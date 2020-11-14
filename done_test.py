#!/usr/bin/python3

import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
GPIO.setup(26, GPIO.OUT)           # set GPIO26 as an output   
      
try:  
    while True:  
        GPIO.output(26, 1)         # set GPIO26 to 1/GPIO.HIGH/True  
        sleep(0.5)                 # wait half a second  
        GPIO.output(26, 0)         # set GPIO26 to 0/GPIO.LOW/False  
        sleep(0.5)                 # wait half a second  
      
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program  
