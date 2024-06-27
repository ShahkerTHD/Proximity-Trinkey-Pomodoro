# Pomodoro Timer V17 by Shaheer on Adafruit Proximity Trinkey

import time
import board
import neopixel
import touchio

# Touch input setup
touch_one = touchio.TouchIn(board.TOUCH1)
touch_two = touchio.TouchIn(board.TOUCH2)

# NeoPixel setup
pixels = neopixel.NeoPixel(board.NEOPIXEL,  2)

# Time durations (in seconds)
WORK_TIME =  1 *  10  #  30 minutes  30 *  60
SHORT_BREAK_TIME =  1 *  5  #  15 minutes  15 *  60
LONG_BREAK_TIME =  1 *  10  #  30 minutes  30 *  60
RGB_TIME =  10  #  10 seconds for RGB effect

# State machine states
STATE_WORK =  0
STATE_SHORT_BREAK =  1
STATE_LONG_BREAK =  2
STATE_RGB =  3

# Start in work state
current_state = STATE_WORK

def work_session():
    pixels.fill((255,  255,  0))  # Yellow light for work
    time.sleep(WORK_TIME)

def short_break():
    pixels.fill((0,  255,  255))  # Cyan light for short break
    time.sleep(SHORT_BREAK_TIME)

def long_break():
    pixels.fill((0,  0,  255))  # Blue light for long break
    time.sleep(LONG_BREAK_TIME)

def rgb_effect():
    for j in range(3):
        for i in range(256):
            pixels[0] = (i,  255,  255 - i)
            pixels[1] = (255 - i, i,  255)
            time.sleep(0.01)
    pixels.fill((0,  0,  0))  # Turn off the lights after RGB effect

while True:
    # Work session
    if current_state == STATE_WORK:
        work_session()
        current_state = STATE_RGB  # Transition to RGB state after work

    # RGB state
    elif current_state == STATE_RGB:
        rgb_effect()
        start_time = time.monotonic()
        while time.monotonic() - start_time < RGB_TIME:
            if touch_one.value:
                current_state = STATE_SHORT_BREAK  # Go to short break if pad  1 pressed during RGB
                break
            elif touch_two.value:
                current_state = STATE_LONG_BREAK  # Go to long break if pad  2 pressed during RGB
                break
            time.sleep(0.1)
        else:
            current_state = STATE_WORK  # No touch detected, go back to work state

    # Short break
    elif current_state == STATE_SHORT_BREAK:
        short_break()
        current_state = STATE_WORK  # Reset to work state after short break

    # Long break
    elif current_state == STATE_LONG_BREAK:
        long_break()
        current_state = STATE_WORK  # Reset to work state after long break

    time.sleep(0.1)
