#!/usr/bin/python
import sys
import pygame as pg
import os
import time
     
     
def play_music(music_file):
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except:
        print("File {} not found! {}".format(music_file, pg.get_error()))
        print "error"
        return
     
    pg.mixer.music.play()
        
    while pg.mixer.music.get_busy():
        clock.tick(30)
     
     
freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)
pg.mixer.init(freq, bitsize, channels, buffer)
     
     
if len(sys.argv) > 1:
     
    try: 
        user_volume = float(sys.argv[1])
    except ValueError:
        print "Volume argument invalid. Please use a float (0.0 - 1.0)"
        pg.mixer.music.fadeout(1000)
        pg.mixer.music.stop()
        raise SystemExit
     
    print("Playing at volume: " + str(user_volume)+ "\n")
    pg.mixer.music.set_volume(user_volume)
    mp3s = []
    for file in os.listdir("./audio"):
        if file.endswith(".mp3"):
            mp3s.append(file)
     
    print mp3s
     
    for x in mp3s: 
        try:
            print "playing " + x
            play_music(x)
            time.sleep(.25)
        except KeyboardInterrupt:
            # if user hits Ctrl/C then exit
            # (works only in console mode)
            pg.mixer.music.fadeout(1000)
            pg.mixer.music.stop()
            raise SystemExit
else:
    print("Please specify volume as a float! (0.0 - 1.0)")
