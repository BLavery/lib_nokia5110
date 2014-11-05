# This example uses fonts found on your PC. (Including any size, and incl proportional fonts)
# ** NOTE **:   You MAY need to edit the font filenames below to suit your PC.
# rPi and Linux: likely in /usr/share/fonts/truetype/    Look for ttf files there.
# Windows: likely in C:\Windows\Fonts\
# (Those 2 locations are used automatically in code below.)
# Fonts listed here were among fonts I found on my own PCs. YMMV

# Demo:
# 1. Use PIL library to draw text (assorted fonts from PC) on an image canvas
#       And then send that graphic canvas to the 5110 display.
# 2. Draw mixed shapes (ellipse) and text on image canvas

# This example works for either rpi GPIO or virtualGPIO


from smartGPIO import GPIO
from lib_nokia5110 import NokiaSPI, Image, ImageDraw, ImageFont
import time
import os, platform

if GPIO.RPI_REVISION == 0:   # VIRTUAL-GPIO
    CE =  10    # VirtGPIO: the chosen Chip Select pin#. (different from rpi)
    DC =   9
    RST =  7
    LED =  6
    spidev = GPIO
    # the virtual GPIO module directly supports spidev function

else:   # RPI
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    CE =   0    # RPI GPIO: 0 or 1 for CE0 / CE1 number (NOT the pin#)
    DC =  22    # Labeled on board as "A0"   Command/Data select
    RST = 23    # RST may use direct +3V strapping, and then be listed as 0 here. (Soft Reset used instead)
    LED = 18    # LED may also be strapped direct to +3V, (and then LED=0 here). LED sinks 10-14 mA @ 3V
    import spidev

#  Don't forget the other 2 SPI pins SCK and MOSI (SDA)

noki = NokiaSPI(GPIO, spidev.SpiDev(), CE, DC, RST, LED)

noki.cls()
noki.set_brightness(100)

print ("Custom character (bell)")

# Test a custom character for 0x7f (supposed to be a bell)
# . . . - - - - -
# . . . - - X - -
# . . . - X X X -
# . . . - X - X -
# . . . X - - - X
# . . . X X X X X
# . . . - - X X -
# . . . - - - - -
noki.define_custom([0x30,0x2c,0x66,0x6c,0x30])
# A slight side-track to start with !!!

noki.cls()
noki.text("\x7f \x7f \x7f \x7f \x7f \x7f \x7f ")  # prints custom character
noki.text("    Hello     ")
if GPIO.RPI_REVISION > 0:
    noki.text(" Raspberry Pi ")
else:
    noki.text(" virtual GPIO ")
noki.text("\n\n6 Line X 14 ch")
# This text was printed directly to 5110 device. Only the one coded monospaced font is available.

time.sleep(4)

# Following text is composed on PIL image (84x48), then sent as whole canvas to 5110 device:
# Any truetype font existing on this PC may be used.
noki.cls()
print ("Image library, 'draw' text with some TTF fonts found on this PC")
# load some available True Type fonts from RPI or PC font collection
# New b-w image
im = Image.new('1', (84,48))   # Here is the 84x48 canvas we will draw upon.
# New drawable on image
draw = ImageDraw.Draw(im)      # And here is the drawing engine that works on our canvas "im"
# ImageDraw has lots of good functions to use.
# Read the PIL documentation.   eg    http://pillow.readthedocs.org/en/latest/reference/
# Only .text() and .ellipse() are used in this example script below.

draw.text((0,0), "ABCdef", fill=1)            # default FONT


# Testing an assortment of font faces:

try:
    if platform.system() == 'Windows':
        fontDir = os.environ['windir'] + "\\Fonts\\"  # Commonly C:\Windows\Fonts\
        font = ImageFont.truetype(fontDir + 'arial.ttf', 18)
        draw.text((15,7), "GHj", font=font, fill=1) # selected font
        font = ImageFont.truetype(fontDir + 'arial.ttf', 10)
        draw.text((0,22), "MNOpqr", font=font, fill=1)
        font = ImageFont.truetype(fontDir + "times.ttf", 12)
        draw.text((20,27), "STUvwx", font=font, fill=1)
        font = ImageFont.truetype(fontDir + "verdana.ttf", 12)
        draw.text((0,36), "YZa%", font=font, fill=1)
        font = ImageFont.truetype(fontDir + "couri.ttf", 10)
        draw.text((40,35), "Abc123", font=font, fill=1)
        font = ImageFont.truetype(fontDir + "georgiai.ttf", 30)
        draw.text((51,0), "Jo", font=font, fill=1)

    else:  # Linux, RPI
        fontDir = "/usr/share/fonts/truetype/"    # Or (gasp) your system may have fonts somewhere else.
        font = ImageFont.truetype(fontDir + "freefont/FreeSans.ttf", 18)
        draw.text((15,7), "GHj", font=font, fill=1) # selected  font
        font = ImageFont.truetype(fontDir + "freefont/FreeSans.ttf", 8)
        draw.text((0,22), "MNOpqr", font=font, fill=1)
        font = ImageFont.truetype(fontDir + "freefont/FreeMono.ttf", 12)
        draw.text((20,27), "STUvwx", font=font, fill=1)
        font = ImageFont.truetype(fontDir + "droid/DroidSansMono.ttf", 12)
        draw.text((0,36), "YZa%", font=font, fill=1)

        # On Linux (incl Raspberry Pi) install ttf-mscorefonts-installer to get Courier & Georgia ...
        # and Arial, Times Roman, Verdana etc, as per classic Windows fonts.
        # These next two are from those extra fonts:
        font = ImageFont.truetype(fontDir + "msttcorefonts/Courier_New.ttf", 10)
        draw.text((40,35), "Abc123", font=font, fill=1)
        font = ImageFont.truetype(fontDir + "msttcorefonts/Georgia_Italic.ttf", 30)
        draw.text((51,0), "Jo", font=font, fill=1)


except:
    print ("At least one of the fonts requested is not on your PC. Edit font filenames for your PC.")

noki.show_image(im)
# clean up
del draw
del im
time.sleep(6)




## Generate an image with PIL - put text with a shape (ellipse), and put on the display
## This demonstrates that the PIL draw method can do much more than text.

print ("Generate image ... ")
print ("(ellipses + 2 fonts)")
# load an available True Type font from RPI font collection
if platform.system() == "Windows":
    font = ImageFont.truetype(fontDir + 'ariali.ttf', 16)
else:
    font = ImageFont.truetype(fontDir + "freefont/FreeSansOblique.ttf", 14)

# New b-w image
im = Image.new('1', (84,48))
# New drawable on image
draw = ImageDraw.Draw(im)
# Full screen and half-screen ellipses
draw.ellipse((0,0,im.size[0]-1,im.size[1]-1), outline=1)
draw.ellipse((im.size[0]/4,im.size[1]/4,im.size[0]/4*3-1,im.size[1]/4*3-1), outline=1)
# Some simple text for a test (first with TT font, second with default
draw.text((10,10), "hello", font=font, fill=1) # selected font
draw.text((10,24), "world", fill=1)            # default FONT
# Check what happens when text exceeds width (clipped)
draw.text((0,0), "ABCabcDEFdefGHIghi", fill=1)
# Copy it to the display
noki.show_image(im)
# clean up
del draw
del im
print ('PIL Drawing')
