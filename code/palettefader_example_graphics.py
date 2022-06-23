# SPDX-FileCopyrightText: 2022-06-23 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
#
# palettefader_example_graphics.py

import displayio
import random
import time
import terminalio
from adafruit_display_text.label import Label
from adafruit_display_shapes.rect import Rect
import adafruit_imageload
from cedargrove_palettefader import PaletteFader

PERSISTENT_BACKGROUND = True  # False for 3-second splash screen

# fmt: off
# Define a few colors
YELLOW  = 0xFFFF00  # temperature
BLUE    = 0x0066FF  # description
AQUA    = 0x00FFFF  # humidity
FUCHSIA = 0xFF00FF  # wind
TEAL    = 0x008080  # other stuff

# Define display parameters
DISPLAY_FONT       = terminalio.FONT
ICON_SPRITESHEET   = "weather-icons0.bmp"
ICON_SPRITE_WIDTH  = 16
ICON_SPRITE_HEIGHT = 16
# fmt: on


class DisplayGraphics(displayio.Group):
    """Creates the palettefader example display layout. Fills the text
    labels and initializes the weather icon. Provides the display brightness
    get/set property as well as random information creation and description
    field scrolling functions."""

    def __init__(self, display, *, brightness=1.0, gamma=1.0):
        super().__init__()

        # A list of named compass directions for use with wind speed
        self._compass = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        # Define initial display parameters
        self.display = display
        display.rotation = 270
        self._brightness = brightness
        self._disp_gamma = gamma
        self._disp_center = (display.width // 2, display.height // 2)

        # Load a background image and create a source_color palette for fader control
        bkg_bitmap, bkg_palette_source = adafruit_imageload.load(
            "loading0.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        # Adjust palette colors in proportion to brightness setting
        bkg_palette_norm = PaletteFader(
            bkg_palette_source, self._brightness - 0.2, gamma=0.65, normalize=True
        )
        bkg_tile = displayio.TileGrid(bkg_bitmap, pixel_shader=bkg_palette_norm.palette)

        self._bkg_group = displayio.Group()
        self._bkg_group.append(bkg_tile)

        if not PERSISTENT_BACKGROUND:
            display.show(self._bkg_group)
            time.sleep(3)  # display startup image for a bit

        self._root_group = displayio.Group()
        self._root_group.append(self)

        if PERSISTENT_BACKGROUND:
            self.append(self._bkg_group)

        self._text_group = displayio.Group()
        self.append(self._text_group)
        self._icon_group = displayio.Group()
        self.append(self._icon_group)

        self.display.show(self._root_group)

        # Create an icon spritesheet and source palette for brightness control
        icon_spritesheet, self.icons_palette_source = adafruit_imageload.load(
            ICON_SPRITESHEET, bitmap=displayio.Bitmap, palette=displayio.Palette
        )
        # Set transparency for palette index 0
        self.icons_palette_source.make_transparent(0)

        # Instantiate icon palette normalizer object and adjust
        self.icon_normal = PaletteFader(
            self.icons_palette_source, self._brightness, gamma=1.0, normalize=True
        )
        self._icon_sprite_tile = displayio.TileGrid(
            icon_spritesheet,
            pixel_shader=self.icon_normal.palette,
            tile_width=ICON_SPRITE_WIDTH,
            tile_height=ICON_SPRITE_HEIGHT,
        )

        # Place a blank icon on-screen
        self._icon_sprite_tile.x = self._disp_center[0] - 8
        self._icon_sprite_tile.y = 12

        self._text_group_colors_source = []
        self._font = DISPLAY_FONT

        self.watchdog = Rect(0, 0, 3, 3, fill=TEAL)
        self._text_group.append(self.watchdog)
        self._text_group_colors_source.append(self.watchdog.fill)

        # Define the text labels. Add an attribute for the group items palette.
        self.temperature_text = Label(self._font)
        self.temperature_text.anchor_point = (0.5, 0.5)
        self.temperature_text.anchored_position = (self._disp_center[0], 4)
        self.temperature_text.color = YELLOW
        self._text_group.append(self.temperature_text)
        self._text_group_colors_source.append(self.temperature_text.color)

        self.description_text = Label(self._font)
        self.description_text.anchor_point = (0.5, 0.5)
        self.description_text.anchored_position = (self.display.width, 55)
        # Use a fixed description like "Overcast clouds"
        self.description_text.text = "The weather outside is frightful"
        self.description_text.color = BLUE
        self._text_group.append(self.description_text)
        self._text_group_colors_source.append(self.description_text.color)

        self.humidity_text = Label(self._font)
        self.humidity_text.anchor_point = (0.5, 0.5)
        self.humidity_text.anchored_position = (self._disp_center[0], 45)
        self.humidity_text.color = AQUA
        self._text_group.append(self.humidity_text)
        self._text_group_colors_source.append(self.humidity_text.color)

        self.wind_text = Label(self._font)
        self.wind_text.anchor_point = (0.5, 0.5)
        self.wind_text.anchored_position = (self._disp_center[0], 34)
        self.wind_text.color = FUCHSIA
        self._text_group.append(self.wind_text)
        self._text_group_colors_source.append(self.wind_text.color)

        self._text_group_palette_norm = PaletteFader(
            self._text_group_colors_source, self._brightness, gamma=1.0, normalize=False
        )

        # Adjust relative brightness of all display objects
        self.brightness = self._brightness

    def scroll_desc(self):
        """Starting at the right-most position on the display, scroll the
        description text one pixel position to the left. Wrap the text after it
        fully disappears. A non-blocking method."""
        self._text_width = self.description_text.bounding_box[2]
        self.description_text.x = self.description_text.x - 1
        if self.description_text.x < 0 - self._text_width:
            self.description_text.x = self.display.width

    def update_info(self):
        """Display random weather information and icon."""

        # Randomly pick a new icon sprite
        if self._icon_group:
            self._icon_group.pop()
        self._icon_sprite_tile[0] = random.randrange(0, 9)
        self._icon_group.append(self._icon_sprite_tile)

        # Make up a temperature value
        temperature = random.randrange(500, 1000) / 10
        self.temperature_text.text = f"{temperature:.0f}°"

        # Make up a relative humidity value
        humidity = random.randrange(200, 900) / 10
        self.humidity_text.text = f"{humidity:.0f}%"

        # Get a direction, determine compass heading, and merge with windspeed
        wind_dir = self._compass[int(((random.randrange(0, 360) + 22.5) % 360) / 45)]
        self.wind_text.text = f"{wind_dir} {random.randrange(0, 250) / 10:.0f}"

        self.display.show(self._root_group)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, new_brightness=1.0):
        """Adjust brightness of all display objects; text colors and weather icon."""
        if True:
            self._brightness = new_brightness

            # Adjust colors and palettes; hide if brightness is < 0.04
            if self._brightness >= 0.04:
                self._icon_group.hidden = False
                self._text_group.hidden = False

                # Adjust brightness of colors of the displayio text group
                self._text_group_palette_norm.brightness = self._brightness

                for i in range(len(self._text_group)):
                    if hasattr(self._text_group[i], "color"):
                        self._text_group[
                            i
                        ].color = self._text_group_palette_norm.palette[i]
                    elif hasattr(self._text_group[i], "fill"):
                        self._text_group[
                            i
                        ].fill = self._text_group_palette_norm.palette[i]

                # Adjust the icon palette brightness and refresh it
                self.icon_normal.brightness = self._brightness
                self._icon_sprite_tile.pixel_shader = self.icon_normal.palette
            else:
                self._icon_group.hidden = True
                self._text_group.hidden = True
