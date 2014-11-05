# MINIMAL example

# Tie LED on 5110 to GND (LED stays on)
# This example is configured just for virtual GPIO

import virtGPIO as GPIO
from lib_nokia5110 import NokiaSPI
from time import sleep

CE =  10    # VirtGPIO: the chosen Chip Select pin#.
DC =   9
RST =  7

#  Don't forget the other 2 SPI pins SCK and MOSI/SDA

noki = NokiaSPI(GPIO, GPIO.SpiDev(), CE, DC, RST)   # GPIO   spidev  CE  DC  RST

noki.cls()
noki.text("--------------")
noki.text("    Hello     ")
noki.text(" virtual GPIO ")
noki.text("\n\n6 Line X 14 ch")
