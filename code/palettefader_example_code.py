# SPDX-FileCopyrightText: 2022-06-20 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
#
# palettefader_example_code.py

"""
This is a PaletteFader class example for a 32x64 RGB LED display panel driven
by an Adafruit Matrix Portal. Four text labels, a shape, and a selectable
spritesheet tile were placed on the display in layers over a normalized, dimmed,
and gamma-corrected background image. The Matrix Portal's UP and DOWN buttons or
the analog voltage on pin A0 control the text and graphic layer brightness over
the fixed-brightness background image.
"""
import time
import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from adafruit_matrixportal.matrix import Matrix
import neopixel
from simpleio import map_range

# pylint: disable=wrong-import-position
from palettefader_example_graphics import DisplayGraphics

ANALOG_FADER = True  # True to enable board.A0 analog brightness control

# fmt: off
# Display settings
DISPLAY_BRIGHTNESS = 0.3  # 0.1 minimum; 1.0 maximum
DISPLAY_GAMMA      = 1.0  # Best for RGB matrix graphics objects (non-images)
DISPLAY_BIT_DEPTH  = 6    # Default is 2-bits; maximum of 6-bits
SCROLL_DELAY       = 0.1  # Description scroll delay (seconds)
# fmt: on

# Instantiate pushbuttons
button_down = DigitalInOut(board.BUTTON_DOWN)
button_down.switch_to_input(pull=Pull.UP)

button_up = DigitalInOut(board.BUTTON_UP)
button_up.switch_to_input(pull=Pull.UP)

# Instantiate fader_control potentiometer
fader_control = AnalogIn(board.A0)

# Instantiate NeoPixel (just in case it's needed)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

# Instantiate RGB LED display panel
matrix = Matrix(bit_depth=DISPLAY_BIT_DEPTH)  # default is 2; maximum is 6

display = DisplayGraphics(
    matrix.display,
    brightness=DISPLAY_BRIGHTNESS,
    gamma=DISPLAY_GAMMA,
)

info_refresh_time = None
scroll_refresh_time = None

while True:
    # Update the on-screen information every 10 seconds (and on first run)
    if (not info_refresh_time) or (time.monotonic() - info_refresh_time) > 10:
        display.update_info()
        info_refresh_time = time.monotonic()

    # Scroll the description every SCROLL_DELAY seconds (and on first run)
    # Adjust brightness with up-down buttons or potentiometer during scrolling
    if (not scroll_refresh_time) or (
        time.monotonic() - scroll_refresh_time
    ) > SCROLL_DELAY:
        display.scroll_desc()
        scroll_refresh_time = time.monotonic()

        if not button_up.value:
            display.brightness = min(display.brightness + 0.01, 1.0)
            print(f"display brightness: {display.brightness:0.2f}")
        if not button_down.value:
            display.brightness = max(display.brightness - 0.01, 0.00)
            print(f"display brightness: {display.brightness:0.2f}")

        if ANALOG_FADER:
            display.brightness = map_range(fader_control.value, 300, 54000, 0.00, 1.0)
            # print(f"fader_control.value: {fader_control.value:6.0f}")
            print(f"display brightness : {display.brightness:6.3f}")
