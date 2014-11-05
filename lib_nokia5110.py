
#    lib_nokia5110.py
# Requires: either virtualGPIO or Raspberry Pi GPIO
#           python 2.7
#           spidev module (for RPi)
#           Pillow (PIL) module

import sys

if __name__ == '__main__':
    print (sys.argv[0], 'is an importable module:')
    print ("...  from", sys.argv[0], "import NokiaSPI")
    print ("")
    exit()





import time
import os

GPIO = None

try:
    from PIL import Image,ImageDraw,ImageFont
except:
    print ("PIL not loaded")
    pass
# PIL is used in "graphics" Font mode
# Failure to load PIL is benign for using only dev-example-nokia5110.py (non graphics)
#       but gives errors if using dev-example-nokia5110-grfxFonts.py

# Display size
ROWS = 6 # Times 8 bits = 48 pixels
CHAR_COLUMNS = 14 # Times 6 pixels = 84 pixels
COLUMNS_PER_CHAR = 6 # Each char is 6 cols wide
COLUMNS = CHAR_COLUMNS * COLUMNS_PER_CHAR
ON = 1
OFF = 0


CLSBUF = [0] * (ROWS * COLUMNS)  # ie 504

# font for regular text() or display_char() functions (ie NOT graphics mode)
_FONT = {
        ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
        '!': [0x00, 0x00, 0x5f, 0x00, 0x00],
        '"': [0x00, 0x07, 0x00, 0x07, 0x00],
        '#': [0x14, 0x7f, 0x14, 0x7f, 0x14],
        '$': [0x24, 0x2a, 0x7f, 0x2a, 0x12],
        '%': [0x23, 0x13, 0x08, 0x64, 0x62],
        '&': [0x36, 0x49, 0x55, 0x22, 0x50],
        "'": [0x00, 0x05, 0x03, 0x00, 0x00],
        '(': [0x00, 0x1c, 0x22, 0x41, 0x00],
        ')': [0x00, 0x41, 0x22, 0x1c, 0x00],
        '*': [0x14, 0x08, 0x3e, 0x08, 0x14],
        '+': [0x08, 0x08, 0x3e, 0x08, 0x08],
        ',': [0x00, 0x50, 0x30, 0x00, 0x00],
        '-': [0x08, 0x08, 0x08, 0x08, 0x08],
        '.': [0x00, 0x60, 0x60, 0x00, 0x00],
        '/': [0x20, 0x10, 0x08, 0x04, 0x02],
        '0': [0x3e, 0x51, 0x49, 0x45, 0x3e],
        '1': [0x00, 0x42, 0x7f, 0x40, 0x00],
        '2': [0x42, 0x61, 0x51, 0x49, 0x46],
        '3': [0x21, 0x41, 0x45, 0x4b, 0x31],
        '4': [0x18, 0x14, 0x12, 0x7f, 0x10],
        '5': [0x27, 0x45, 0x45, 0x45, 0x39],
        '6': [0x3c, 0x4a, 0x49, 0x49, 0x30],
        '7': [0x01, 0x71, 0x09, 0x05, 0x03],
        '8': [0x36, 0x49, 0x49, 0x49, 0x36],
        '9': [0x06, 0x49, 0x49, 0x29, 0x1e],
        ':': [0x00, 0x36, 0x36, 0x00, 0x00],
        ';': [0x00, 0x56, 0x36, 0x00, 0x00],
        '<': [0x08, 0x14, 0x22, 0x41, 0x00],
        '=': [0x14, 0x14, 0x14, 0x14, 0x14],
        '>': [0x00, 0x41, 0x22, 0x14, 0x08],
        '?': [0x02, 0x01, 0x51, 0x09, 0x06],
        '@': [0x32, 0x49, 0x79, 0x41, 0x3e],
        'A': [0x7e, 0x11, 0x11, 0x11, 0x7e],
        'B': [0x7f, 0x49, 0x49, 0x49, 0x36],
        'C': [0x3e, 0x41, 0x41, 0x41, 0x22],
        'D': [0x7f, 0x41, 0x41, 0x22, 0x1c],
        'E': [0x7f, 0x49, 0x49, 0x49, 0x41],
        'F': [0x7f, 0x09, 0x09, 0x09, 0x01],
        'G': [0x3e, 0x41, 0x49, 0x49, 0x7a],
        'H': [0x7f, 0x08, 0x08, 0x08, 0x7f],
        'I': [0x00, 0x41, 0x7f, 0x41, 0x00],
        'J': [0x20, 0x40, 0x41, 0x3f, 0x01],
        'K': [0x7f, 0x08, 0x14, 0x22, 0x41],
        'L': [0x7f, 0x40, 0x40, 0x40, 0x40],
        'M': [0x7f, 0x02, 0x0c, 0x02, 0x7f],
        'N': [0x7f, 0x04, 0x08, 0x10, 0x7f],
        'O': [0x3e, 0x41, 0x41, 0x41, 0x3e],
        'P': [0x7f, 0x09, 0x09, 0x09, 0x06],
        'Q': [0x3e, 0x41, 0x51, 0x21, 0x5e],
        'R': [0x7f, 0x09, 0x19, 0x29, 0x46],
        'S': [0x46, 0x49, 0x49, 0x49, 0x31],
        'T': [0x01, 0x01, 0x7f, 0x01, 0x01],
        'U': [0x3f, 0x40, 0x40, 0x40, 0x3f],
        'V': [0x1f, 0x20, 0x40, 0x20, 0x1f],
        'W': [0x3f, 0x40, 0x38, 0x40, 0x3f],
        'X': [0x63, 0x14, 0x08, 0x14, 0x63],
        'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
        'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
        '[': [0x00, 0x7f, 0x41, 0x41, 0x00],
        '\\': [0x02, 0x04, 0x08, 0x10, 0x20],
        ']': [0x00, 0x41, 0x41, 0x7f, 0x00],
        '^': [0x04, 0x02, 0x01, 0x02, 0x04],
        '_': [0x40, 0x40, 0x40, 0x40, 0x40],
        '`': [0x00, 0x01, 0x02, 0x04, 0x00],
        'a': [0x20, 0x54, 0x54, 0x54, 0x78],
        'b': [0x7f, 0x48, 0x44, 0x44, 0x38],
        'c': [0x38, 0x44, 0x44, 0x44, 0x20],
        'd': [0x38, 0x44, 0x44, 0x48, 0x7f],
        'e': [0x38, 0x54, 0x54, 0x54, 0x18],
        'f': [0x08, 0x7e, 0x09, 0x01, 0x02],
        'g': [0x0c, 0x52, 0x52, 0x52, 0x3e],
        'h': [0x7f, 0x08, 0x04, 0x04, 0x78],
        'i': [0x00, 0x44, 0x7d, 0x40, 0x00],
        'j': [0x20, 0x40, 0x44, 0x3d, 0x00],
        'k': [0x7f, 0x10, 0x28, 0x44, 0x00],
        'l': [0x00, 0x41, 0x7f, 0x40, 0x00],
        'm': [0x7c, 0x04, 0x18, 0x04, 0x78],
        'n': [0x7c, 0x08, 0x04, 0x04, 0x78],
        'o': [0x38, 0x44, 0x44, 0x44, 0x38],
        'p': [0x7c, 0x14, 0x14, 0x14, 0x08],
        'q': [0x08, 0x14, 0x14, 0x18, 0x7c],
        'r': [0x7c, 0x08, 0x04, 0x04, 0x08],
        's': [0x48, 0x54, 0x54, 0x54, 0x20],
        't': [0x04, 0x3f, 0x44, 0x40, 0x20],
        'u': [0x3c, 0x40, 0x40, 0x20, 0x7c],
        'v': [0x1c, 0x20, 0x40, 0x20, 0x1c],
        'w': [0x3c, 0x40, 0x30, 0x40, 0x3c],
        'x': [0x44, 0x28, 0x10, 0x28, 0x44],
        'y': [0x0c, 0x50, 0x50, 0x50, 0x3c],
        'z': [0x44, 0x64, 0x54, 0x4c, 0x44],
        '{': [0x00, 0x08, 0x36, 0x41, 0x00],
        '|': [0x00, 0x00, 0x7f, 0x00, 0x00],
        '}': [0x00, 0x41, 0x36, 0x08, 0x00],
        '~': [0x10, 0x08, 0x08, 0x10, 0x08],
        '\x7f': [0x00, 0x7e, 0x42, 0x42, 0x7e],
}

ORIGINAL_CUSTOM = _FONT['\x7f']

def _bit_reverse(value, width=8):
        ''' Reverse the bits in a byte '''
        result = 0
        for _ in range(width):
                result = (result << 1) | (value & 1)
                value >>= 1

        return result

_BITREVERSE = map(_bit_reverse, range(256))


class NokiaSPI:
        def __init__(self, gpio, spidev, cePin, dcPin, rstPin, ledPin=0, speed=5000000, brightness=100, contrast=0xb0):
                global GPIO
                GPIO = gpio
                self.CE = cePin
                self.dc = dcPin
                self.rst = rstPin
                self.ledpin = ledPin
                self.spi = spidev
                self.spi.open(0, self.CE)

                self.speed = speed
                self.spi.max_speed_hz=self.speed

                # Set pin directions.
                for pin in [self.dc, self.rst, self.ledpin]:
                        GPIO.setup(pin, GPIO.OUT)

                self.contrast=contrast
                self.brightness=brightness

                # Toggle RST low to reset.
                GPIO.output(self.rst, OFF)
                time.sleep(0.100)
                GPIO.output(self.rst, ON)

                # Initialise LCD
                # 0x21 = Function set (0x20) + Power-down mode (0x04) + Vertical addressing (0x02) + Extended instruction set (0x01)
                # 0x14 = Bias system (0x10) + BS2 (0x04) + BS1 (0x02) + BS0 (0x01)
                # 0xXX = Vop (Operation Voltage) = 0x80 + 7 bits
                # 0x20 = Back to basic instruction set
                # 0x0c = Display Control = 0x08 + 3 bits: D,0,E. 0x04 = Normal mode
                self.lcd_cmd([0x21, 0x14, self.contrast, 0x20, 0x0c])

                self.row = -1
                self.col = -1
                # Clear the screen. This will also initialise self.row and self.col
                self.cls()

                if GPIO.RPI_REVISION > 0:
                    GPIO.output(ledPin, GPIO.LOW)
                else:
                    GPIO.pwmWrite(self.ledpin, 50)  #  frequency=50Hz
                    self.set_brightness(self.brightness)


        def lcd_cmd(self,value):
                ''' Write a value or list of values to the LCD in COMMAND mode '''
                GPIO.output(self.dc, OFF)
                if type(value) != type([]):
                        value = [value]
                self.spi.writebytes(value)


        def lcd_data(self,value):
                ''' Write a value or list of values to the LCD in DATA mode '''
                GPIO.output(self.dc, ON)
                if type(value) != type([]):
                        value = [value]
                self.spi.writebytes(value)
                # Calculate new row/col
                # Writing off the end of a row proceeds to the next row
                # Writing off the end of the last row proceeds to the first row
                self.row = (self.row + ((self.col + len(value)) // COLUMNS)) % ROWS
                self.col = (self.col + len(value)) % COLUMNS


        def gotoxy(self, x, y):
                ''' Move the cursor (in memory) to position x, y '''
                assert(0 <= x <= COLUMNS)
                assert(0 <= y <= ROWS)
                # 0x80 = Set X ram address
                # 0x40 = Set Y ram address
                self.lcd_cmd([x+128,y+64])
                self.col = x
                self.row = y


        def cls(self):
                ''' Clear the entire display '''
                self.gotoxy(0, 0)
                self.lcd_data(CLSBUF)
                # Note, we wrote EXACTLY the right number of 0's to return to 0,0



        def fill(self,pattern=0xff):
                fillbuf=[pattern]*(ROWS * COLUMNS)
                self.gotoxy(0, 0)
                self.lcd_data(fillbuf)


        def set_brightness(self, led_value):
                #Set the backlight LED brightness. Valid values are 0 <-> 100
                # On virt GPIO, use PWM to vary brightness. On RPI, <50% = off, >50% = on
                assert(0 <= led_value <= 100)
                if GPIO.RPI_REVISION > 0:
                    GPIO.output(self.ledpin, (led_value <50))
                else:
                    GPIO.pwmWrite(self.ledpin, 255 - (led_value*25)//10)
                    if led_value == 100:
                        GPIO.output(self.ledpin, 0)
                self.brightness = led_value


        def set_contrast(self, value):
                ''' Set the contrast. Valid values are 0x80 <-> 0xFF '''
                assert(0x80 <= value <= 0xFF)
                self.lcd_cmd([0x21, value, 0x20])
                self.contrast = value



        def show_custom(self):
                ''' Display the custom char from [font] '''
                self.display_char('\x7f', _FONT)


        def define_custom(self, values):
                ''' Overwrite the custom char value in the default font '''
                _FONT['\x7f'] = values


        def restore_custom(self):
                ''' Restore the custom char value to it's default in the default font '''
                self.define_custom(ORIGINAL_CUSTOM)

        def next_row(self):
                ''' Return the next row, accounting for page wrapping '''
                return (self.row + 1) % ROWS

        def next_col(self):
                ''' Return the next pixel column, accounting for line wrapping '''
                return (self.col + 1) % COLUMNS

        def char_col(self):
                ''' Return the cahracter column (as opposed to self.col which is a pixel column counter) '''
                return self.col // COLUMNS_PER_CHAR

        def next_char_col(self):
                ''' Return the next character column, accounting for line wrapping '''
                return (self.char_col() + 1) % CHAR_COLUMNS


        def display_char(self, char):
                ''' Display a single character. Carriage return clears the remainder of the line and proceeds to the next row '''
                try:
                        if char == '\n':
                                # Clear the rest of the line. This also puts the cursor at the beginning of the next line.
                                self.lcd_data([0] * (COLUMNS - self.col))
                        else:
                                self.lcd_data(_FONT[char]+[0])

                except KeyError:
                        pass # Ignore undefined characters.


        def text(self, string, wrap=True):
                '''
                Display a string of text.
                If wrap is False lines longer than COLUMNS will be truncated and lines beyond ROWS will be discarded
                '''
                def truncate(s):
                        ''' Cut off anything beyond CHAR_COLUMNS '''
                        s = s[:CHAR_COLUMNS]
                        if len(s) == CHAR_COLUMNS:
                                return s
                        else:
                                # We only need a carriage return if we were'nt at the end of the line
                                return s+'\n'

                if not wrap:
                        # The following would go strangely if we were in the middle of a char
                        assert(self.col % COLUMNS_PER_CHAR == 0)
                        # We need padding if we're not already at the start of the line
                        pad = '0'*self.char_col()
                        # There a lot going on in this next line, so for those who're having trouble following:
                        #  Combine the pad and the string
                        #  Split it into a list of lines (carriage returns are discarded)
                        #  Throw away any lines beyond ROWS, accounting for the number of rows already displayed
                        #  Run truncate() on each line (this re-provides the carriage returns if required)
                        #  Join the list back together into a string
                        #  Cut off the pad we added at the start
                        string = ''.join([truncate(s) for s in (pad+string).splitlines()[:ROWS-self.row]])[len(pad):]
                for char in string:
                        self.display_char(char)


        def gotorc(self, r, c):
                ''' Move to character row, column '''
                self.gotoxy(c*6,r)


        def centre_word(self, r, word):
                ''' Display 'word' centered in row 'row' '''
                self.gotorc(r, max(0, (CHAR_COLUMNS - len(word)) // 2))
                self.text(word)


        def show_image(self,im):
                ''' Display an image 'im' '''
                # Rotate and mirror the image
                rim = im.rotate(-90).transpose(Image.FLIP_LEFT_RIGHT)

                # Change display to vertical write mode for graphics
                GPIO.output(self.dc, OFF)
                self.spi.writebytes([0x22])

                # Start at upper left corner
                self.gotoxy(0, 0)
                # Put on display with reversed bit order
                GPIO.output(self.dc, ON)
                self.spi.writebytes( [ _BITREVERSE[ord(x)] for x in list(rim.tostring()) ] )

                # Switch back to horizontal write mode for text
                GPIO.output(self.dc, OFF)
                self.spi.writebytes([0x20])


if __name__ == '__main__':
    pass
