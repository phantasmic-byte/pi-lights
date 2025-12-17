import time
import adafruit_fancyled.adafruit_fancyled as fancy
import keyboard
import board
import neopixel

# Initialize variables

# Board type
pixel_board = board.D18

# Number of pixels
num_pixels = 30
num_pixels = 240

# Order of Pixel
ORDER = neopixel.GRB

# Brightness
BRIGHTNESS = 0.2

# Auto Write
AUTOWRITE = False

pixels = neopixel.NeoPixel(
    pixel_board, num_pixels, brightness = BRIGHTNESS, auto_write = AUTOWRITE, pixel_order = ORDER
)


#pixels[0] = (255, 0, 0)
pixels.fill((255, 0, 0))
pixels.show()
def runner(color, len_light, wait):
    for i in range(0, num_pixels):
        for j in range(len_light):
            pixels[(i + j) % num_pixels] = color
        pixels.show()
        time.sleep(wait)
        pixels.fill(0)

def bounce(color, len_light, wait):
    # 1 is forwards, -1 is backwards
    for d in [1, -1]:
        start = 0 if d == 1 else num_pixels - len_light 
        end = num_pixels - len_light if d == 1 else 0 
        for i in range(start, end, d):
            for j in range(len_light):
                pixels[(i + j)] = color
            pixels.show()
            time.sleep(wait)
            pixels.fill(0)

def fade(color, wait, steps):
    for d in [1, -1]:
        start = 0 if d == 1 else steps
        end = steps if d == 1 else 0
        for i in range(start, end, d):
            pixels.fill(tuple(map(lambda x: round(x/steps * i), color)))
            pixels.show()
            time.sleep(wait)

def fade_multicol(colors, wait, step):
    for color in colors:
        fade(color, wait, step)

def hue_wipe(steps, wait):
    for i in range(steps) :
        color = fancy.CHSV(i/steps, 1.0, 0.2).pack() 
        pixels.fill(color)
        pixels.show()
        time.sleep(wait)

# wheel and ranbow_cycle function from https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in {neopixel.RGB, neopixel.GRB} else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

while True:
    #runner((255,0,0), 3, 0.009)
    #bounce((255,0,0), 3, 0.009)
    #fade_multicol([(255,0,0), (0,255,0), (0,0,255)], 0.02, 50)
    #hue_wipe(1000, 0.001)
    rainbow_cycle(0.1)

    # Press 'q' to quit
    if keyboard.is_pressed('q'):
        pixels.fill(0)
        pixels.show()
        break;

