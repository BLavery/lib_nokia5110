# DEMO: Regular text display  -  Single hardcoded monospaced font
# 1. Character set
# 2. Contrast test. Pick your optimum to use in all your own applications
# 3. Brightness test.


# LED pin is optional.  Leave it out (or =0) here, and then tie LED on 5110 to GND.
# On virtual GPIO the LED works best on a PWM pin (eg 6)
# RST pin is not optional. This device sometimes misbehaves if not properly reset by hardware.


from smartGPIO import GPIO
from lib_nokia5110 import NokiaSPI
import time


if GPIO.RPI_REVISION == 0:   # VIRTUAL-GPIO
    spidev = GPIO
    # the virtual GPIO module directly supports spidev function
    noki = NokiaSPI(GPIO, spidev.SpiDev(), 10, 9, 7, 6)   # GPIO spidev CEpin  DC  RST  LED (arduino pins)

else:   # RPI
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    import spidev
    noki = NokiaSPI(GPIO, spidev.SpiDev(), 0, 22, 23, 18)   # GPIO spidev CE0 and BCM RPI numbers

noki.cls()
noki.set_brightness(30)
time.sleep(1)
noki.set_brightness(80)

start, end = 32, 116
print ('LCD Display Test: ASCII %d to %d' % (start, end))
for i in range(start, end):
        noki.display_char(chr(i))

time.sleep(4)
print ('Cls, LED on, %d chars' % (end - start))



noki.cls()
noki.text("--------------")
noki.text("    Hello     ")
if GPIO.RPI_REVISION > 0:
    noki.text(" Raspberry Pi ")
else:
    noki.text(" virtual GPIO ")
noki.text("\n\n6 Line X 14 ch")

time.sleep(4)

# Contrast
print ("LCD Contrast test")
noki.cls()
old_contrast = noki.contrast
#  for i in range(0x80,0xFF):     # Only the middle of the theoretical 80-ff is really useful
for i in range(0xa0,0xCF, 2):     # So we test a0 to cf only. Remember your optimum and use it hereafter.
        noki.set_contrast(i)
        noki.gotorc(2,0)
        noki.text('Contrast:\n%s\n' % hex(i))
        time.sleep(0.4)
noki.set_contrast(old_contrast)

# brightness PWM testing on virtual GPIO    -- off -> 100%
# Note RPI just has on/off (above/below 50%)
print ("LED Brightness test")
noki.cls()
for i in range(0,100,10):
        noki.set_brightness(i)
        noki.gotorc(2,0)
        noki.text("Brightness:\n%s\n" % i)
        time.sleep(0.5)
noki.set_brightness(100)
noki.gotorc(2,0)
noki.text("Brightness:\n%s\n" % 100)
# Why wouldn't we simply use 100% always??

time.sleep(3)
noki.cls()
noki.text("Bye ...")
time.sleep(2)
noki.set_brightness(0)
