# modified version of
# https://raspberrytips.nl/tm1637-4-digit-led-display-raspberry-pi/

import sys
import time
import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

FONTS = {'0':0x3f, '1':0x06, '2':0x5b, '3':0x4f, '4':0x66, '5':0x6d, '6':0x7d, '7':0x07,
         '8':0x7f, '9':0x6f, 'A':0x77, 'b':0x7C, 'B':0x7C, 'C':0x39, 'd':0x5E, 'D':0x5E,
         'E':0x79, 'F':0x71, 'G':0x3D, 'H':0x76, 'I':0x06, 'J':0x1E, 'K':0x76, 'L':0x38,
         'M':0x55, 'n':0x54, 'N':0x54, 'O':0x3F, 'P':0x73, 'q':0x67, 'Q':0x67, 'r':0x50, 'R':0x50,
         'S':0x6D, 't':0x78, 'T':0x78, 'U':0x3E, 'v':0x1C, 'V':0x1C, 'W':0x2A, 'X':0x76,
         'y':0x6E, 'Y':0x6E, 'Z':0x5B, ' ':0x00, '-':0x40, 'Unknown':0x49 }

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44

STARTADDR = 0xC0

BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHT_HIGHEST = 7

OUTPUT = IO.OUT
INPUT = IO.IN

LOW = IO.LOW
HIGH = IO.HIGH

class TM1637:
    __doublePoint = False
    __Clkpin = 0
    __Datapin = 0
    __brightnes = BRIGHT_TYPICAL;
    __currentData = [0,0,0,0];

    def __init__( self, pinClock, pinData, brightnes ):
        self.__Clkpin = pinClock
        self.__Datapin = pinData
        self.__brightnes = brightnes;
        IO.setup(self.__Clkpin,OUTPUT)
        IO.setup(self.__Datapin,OUTPUT)
    # end  __init__

    def Clear(self):
        b = self.__brightnes;
        point = self.__doublePoint;
        self.__brightnes = 0;
        self.__doublePoint = False;
        data = [' ', ' ', ' ', ' ']
        self.Show(data);
        self.__brightnes = b;   # restore saved brightnes
        self.__doublePoint = point;
    # end  Clear

    def Show( self, data ):
        for i in range(0,4):
            self.__currentData[i] = data[i];

        self.start(); self.writeByte(ADDR_AUTO); self.stop(); self.start();
        self.writeByte(STARTADDR);
        for i in range(0,4):
            self.writeByte(self.coding(data[i]));
        self.stop();
        self.start();
        self.writeByte(0x88 + self.__brightnes);
        self.stop();
    # end  Show

    def SetBrightnes(self, brightnes):  # brightnes 0...7
        if( brightnes > 7 ):
            brightnes = 7;
        elif( brightnes < 0 ):
            brightnes = 0;

        if( self.__brightnes != brightnes):
            self.__brightnes = brightnes;
            self.Show(self.__currentData);
        # end if
    # end  SetBrightnes

    def ShowDoublepoint(self, on):  # shows or hides the doublepoint :
        if( self.__doublePoint != on):
            self.__doublePoint = on;
            self.Show(self.__currentData);
        # end if
    # end  ShowDoublepoint

    def writeByte( self, data ):
        for i in range(0,8):
            IO.output( self.__Clkpin, LOW)
            if(data & 0x01):
                IO.output( self.__Datapin, HIGH)
            else:
                IO.output( self.__Datapin, LOW)
            data = data >> 1
            IO.output( self.__Clkpin, HIGH)
        #endfor

        # wait for ACK
        IO.output( self.__Clkpin, LOW)
        IO.output( self.__Datapin, HIGH)
        IO.output( self.__Clkpin, HIGH)
        IO.setup(self.__Datapin, INPUT)

        while(IO.input(self.__Datapin)):
            time.sleep(0.001)
            if( IO.input(self.__Datapin)):
                IO.setup(self.__Datapin, OUTPUT)
                IO.output( self.__Datapin, LOW)
                IO.setup(self.__Datapin, INPUT)
            #endif
        # endwhile
        IO.setup(self.__Datapin, OUTPUT)
    # end writeByte

    def start(self):
        IO.output( self.__Clkpin, HIGH) # send start signal to TM1637
        IO.output( self.__Datapin, HIGH)
        IO.output( self.__Datapin, LOW)
        IO.output( self.__Clkpin, LOW)
    # end start

    def stop(self):
        IO.output( self.__Clkpin, LOW)
        IO.output( self.__Datapin, LOW)
        IO.output( self.__Clkpin, HIGH)
        IO.output( self.__Datapin, HIGH)
    # end stop

    def coding(self, data):
        if ( self.__doublePoint ):
            pointData = 0x80
        else:
            pointData = 0
        
        # 0 ~ 9, A ~ Z, blank, -, 'Unknown'
        if (data in FONTS):
            return FONTS[data] + pointData;
        else:
            return FONTS['Unknown'] + pointData;
    # end coding
# end class TM1637
