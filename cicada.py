#!/usr/bin/python3
######################
# CICADA ART PROJECT #
######################

import smbus
import sys
import pygame as pg
import os
import time
     
#####################
# Definitions start #     
#####################

def int_to_bcd(x):
    return int(str(x)[-2:], 0x10)

def write_time_to_clock(pos, hours, minutes, seconds):
    bus.write_byte_data(DS3231, pos, int_to_bcd(seconds))
    bus.write_byte_data(DS3231, pos + 1, int_to_bcd(minutes))
    bus.write_byte_data(DS3231, pos +2, int_to_bcd(hours))

def set_alarm1_mask_bits(bits):
    pos = ALARM1_SECONDS_REG
    for bit in reversed(bits):
        reg = bus.read_byte_data(DS3231, pos)
        if bit:
            reg = reg | 0x80
        else:
            reg = reg & 0x7F
        bus.write_byte_data(DS3231, pos, reg)
        pos = pos + 1

def enable_alarm1():
    reg = bus.read_byte_data(DS3231, CONTROL_REG)
    bus.write_byte_data(DS3231, CONTROL_REG, reg | 0x05)

def clear_alarm1_flag():
    reg = bus.read_byte_data(DS3231, STATUS_REG)
    bus.write_byte_data(DS3231, STATUS_REG, reg & 0xFE)

def check_alarm1_triggered():
    return bus.read_byte_data(DS3231, STATUS_REG) & 0x01 != 0

# Play music based on file path provided
def play_music(music_file):
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except:
        print("File {} not found! {}".format(music_file, pg.get_error()))
        print("error")
        return
     
    pg.mixer.music.play()
        
    while pg.mixer.music.get_busy():
        clock.tick(30)
     
def set_timer(hours, minutes, seconds):
    # zero the clock
    write_time_to_clock(SECONDS_REG, 0, 0, 0)
    # set the alarm
    write_time_to_clock(ALARM1_SECONDS_REG, hours, minutes, seconds)
    # set the alarm to match hours minutes and seconds
    # need to set some flags
    set_alarm1_mask_bits((True, False, False, False))
    enable_alarm1()
    clear_alarm1_flag()

###################
# DEFINITIONS END #     
###################

# RTC variables
bus = smbus.SMBus(1)
DS3231 = 0x68
SECONDS_REG = 0x00
ALARM1_SECONDS_REG = 0x07
CONTROL_REG = 0x0E
STATUS_REG = 0x0F

# Audio variables
freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)
pg.mixer.init(freq, bitsize, channels, buffer)
     
     
if len(sys.argv) > 4:
     
    # Set volume based on user input
    try: 
        user_volume = float(sys.argv[2])
    except ValueError:
        print("Volume argument invalid. Please use a float (0.0 - 1.0)")
        pg.mixer.music.fadeout(1000)
        pg.mixer.music.stop()
        raise SystemExit
     
    print("Playing at volume: " + str(user_volume)+ "\n")
    pg.mixer.music.set_volume(user_volume)

    # Play the MP3 based on user input
    try:
        print("playing " + sys.argv[1])
        play_music(sys.argv[1])
        time.sleep(.25)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pg.mixer.music.fadeout(1000)
        pg.mixer.music.stop()
        raise SystemExit
    
    # Set the RTC clock to power off/on based on user input
    try:
        with open('/home/pi/wittypi/schedule.wpi', 'w') as f:
            f.write("BEGIN\t2021-08-05 00:00:00\nEND\t2035-07-31 23:59:59\nON\tM" + str(sys.argv[3]) + "\tWAIT\nOFF\tH" + str(sys.argv[4]))
            f.close()
        os.system('/bin/bash /home/pi/wittypi/runScript.sh')        
    except:
        print("An error occurred setting the RTC timer")
else:
    print("Please specify volume as a float! (0.0 - 1.0)")
    print("Command syntax : ./cicada.py <path to mp3 file> <volume: 0.0 - 1.0> <minutes to sleep> <hours to sleep>")

