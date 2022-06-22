#!/usr/bin/python3
"""
Solis Robot - SoBot

Line_Sensor.py: Programming example for the Solis robot to move following a line.

Created By   : Vinicius M. Kawakami
Version      : 1.0

Company: Solis Tecnologia
"""

from time import sleep
import serial

data_line = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

flag_fw = 0
flag_enable = 1
count_bl = 0

black = 49
white = 48

# Set serial port
usb = serial.Serial('/dev/ttyACM0', 57600, timeout=0, dsrdtr=False)
usb.flush()     # Waits data configuration

usb.write(b"LT E1 RD0 GR50 BL0")    # Turn on led tape in green

sleep(2)
usb.write(b"MT0 MC AT100 DT100 V2") # Parameter settings for continuous mode
sleep(1)
usb.write(b"MT0 ME1")               # Enables wheel motors on mode continuous
sleep(1)

while flag_enable == 1:

    usb.write(b"SL")            # Send command to read line sensor
    sleep(0.1)                  # Wait to return datas
    data_line = usb.readline()  # Read data
    print(data_line)

    # Check if sensor 2 is reading black line or if all sensors are reading black
    if(((data_line[4] == white) and (data_line[10] == black) and (data_line[16] == white)) or
     ((data_line[4] == black) and (data_line[10] == black) and (data_line[16] == black))):
        if(flag_fw == 0):
            flag_fw = 1
            usb.write(b"LT E1 RD0 GR50 BL0")
            usb.write(b"MT0 MF")    # Moving to forward

    # Check if sensor 1 and 2 is reading black
    elif((data_line[4] == black) and (data_line[10] == black) and (data_line[16] == white)):
        flag_fw = 0
        count_bl = 0
        usb.write(b"LT E1 RD0 GR0 BL50")
        usb.write(b"MT0 ML")        # Turn left
        sleep(0.6)
        usb.write(b"MT0 MF")
        sleep(0.2)
    # Check if sensor 1 is reading black
    elif((data_line[4] == black) and (data_line[10] == white) and (data_line[16] == white)):
        flag_fw = 0
        count_bl = 0
        usb.write(b"LT E1 RD0 GR0 BL50")
        usb.write(b"MT0 ML")        # Turn left
        sleep(0.9)
        usb.write(b"MT0 MF")
        sleep(0.2)
    # Check if sensor 2 and 3 is reading black
    elif((data_line[4] == white) and (data_line[10] == black) and (data_line[16] == black)):
        flag_fw = 0
        count_bl = 0
        usb.write(b"LT E1 RD0 GR15 BL25")
        usb.write(b"MT0 MR")        # Turn right
        sleep(0.6)
        usb.write(b"MT0 MF")
        sleep(0.2)
    # Check if sensor 3 is reading black
    elif((data_line[4] == white) and (data_line[10] == white) and (data_line[16] == black)):
        flag_fw = 0
        count_bl = 0
        usb.write(b"LT E1 RD0 GR15 BL25")
        usb.write(b"MT0 MR")        # Turn right
        sleep(0.9)
        usb.write(b"MT0 MF")
        sleep(0.2)
    # Check if all sensor is reading white
    elif((data_line[4] == white) and (data_line[10] == white) and (data_line[16] == white)):
        flag_fw = 0
        count_bl += 1
        usb.write(b"LT E1 RD50 GR0 BL0")
        usb.write(b"MT0 MB")        # Moving to back
        sleep(0.5)

        if(count_bl >= 5):
            flag_enable = 0

    data_line = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

usb.write(b"MT0 MP")                # Moviment Pause
sleep(0.5)
usb.write(b"MT0 ME0")               # Disables wheel motors on mode continuous
usb.write(b"LT E1 RD0 GR0 BL0")
sleep(0.5)
usb.write(b"LT E1 RD50 GR0 BL0")
sleep(0.5)
usb.write(b"LT E1 RD0 GR0 BL0")
sleep(0.5)
usb.write(b"LT E1 RD50 GR0 BL0")
sleep(0.5)
usb.write(b"LT E1 RD0 GR0 BL0")
sleep(0.5)
usb.write(b"LT E1 RD50 GR0 BL0")
sleep(0.5)
usb.write(b"LT E1 RD0 GR0 BL0")
usb.write(b"LT E0")