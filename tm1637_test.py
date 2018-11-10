# test for tm1637.py

import time
import datetime
import RPi.GPIO as GPIO
import tm1637

def show_time():
   while(True):
       now = datetime.datetime.now() 
       hour = now.hour
       minute = now.minute
       second = now.second
       currenttime = [ repr(int(hour / 10)), repr(hour % 10),
                       repr(int(minute / 10)), repr(minute % 10) ]

       Display.Show(currenttime)
       Display.ShowDoublepoint(second % 2) # 0, 1

       time.sleep(1)

Display = tm1637.TM1637(23,24,tm1637.BRIGHT_TYPICAL)

Display.Clear() # 
Display.SetBrightnes(2)

Display.Show(['0', '1', '2', '3'])
Display.ShowDoublepoint(0)
time.sleep(3)

Display.Show(['C', 'O', 'O', 'L'])
Display.ShowDoublepoint(1)
time.sleep(3)

Display.Show([' ', '-', '*', 'Unknown'])
Display.ShowDoublepoint(1)
time.sleep(3)

Display.Clear()
show_time()


