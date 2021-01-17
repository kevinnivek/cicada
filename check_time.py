#!/usr/bin/python3
# Workaround to deal with DS3231 RTC -10 hour offset
import os,time
import sys
import datetime
import random
import SDL_DS3231

ds3231 = SDL_DS3231.SDL_DS3231(1, 0x68)

os.system('sudo rmmod rtc_ds1307')
print(ds3231.read_datetime())
os.system('sudo modprobe rtc_ds1307')
#
#current_time=os.system('sudo hwclock -r')
#print(current_time)
#current_unix=`sudo hwclock --verbose | grep "Hw clock time" | awk -F "\= " '{printf "%s\n", $2}' | awk -F " " '{printf "%s\n", $1}'`
#current_date=`date -d "@${current_unix}" -d "+15 hours"`
#start=`date -d "${current_date}" -d "9:00" +"%s"`
#end=`date -d "${current_date}" -d "14:00" +"%s"`

#echo "current date : $current_date"
#echo "start : $start"
#echo "end : $end"
#echo "current : $current_unix"

#if (($current_unix >= $start && $current_unix <= $end)); 
#then
#    echo "within time range"
#else
#    echo "not within time range"
#fi
