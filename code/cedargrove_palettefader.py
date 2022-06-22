# SPDX-FileCopyrightText: Copyright (c) 2022 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_palettefader`
================================================================================

PaletteFader is a CircuitPython driver class for brightness-adjusting displayio
color palettes and lists. Normalization is optionally applied prior to the
brightness and gamma adjustment. Preserves transparency index values. Creates a
displayio color palette object (displayio.Palette).

For adjusting a single color value, create a list containing a single color or
use cedargrove_palettefader.set_color_brightness().

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------

The ulab-based reference palette creation code was adapted from the Adafruit
Ocean Epoxy Lightbox project's Reshader class; Copyright 2020 J Epler and L Fried.
<https://learn.adafruit.com/ocean-epoxy-resin-lightbox-with-rgb-led-matrix-image-scroller>

**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  <https://circuitpython.org/downloads>

"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Palette_Fader.git"

from ulab import numpy
import displayio

import time


class PaletteFader:
    """Displayio palette fader with normalization, brightness (fading), and
    gamma control. Returns an adjusted displayio palette object."""

    def __init__(self, source_palette, brightness=1.0, gamma=1.0, normalize=False):
        """Instantiate the palette fader. Creates a reference numpy array
        containing RGB values derived from the source palette. The palette's
        brightest RGB component value is determined for use by the normalize
        function, if enabled."""

        self._src_palette = source_palette
        self._brightness = brightness
        self._gamma = gamma
        self._normalize = normalize

        # Create the reference palette with separated source palette RGB values
        self._ref_palette = numpy.zeros((len(self._src_palette), 3), dtype=numpy.uint8)
        for index, color in enumerate(self._src_palette):
            rgb = int(self._src_palette[index])
            if rgb is not None:
                self._ref_palette[index, 2] = rgb & 0x0000FF
                self._ref_palette[index, 1] = (rgb & 0x00FF00) >> 8
                self._ref_palette[index, 0] = (rgb & 0xFF0000) >> 16
            else:
                self._ref_palette[index] = [None, None, None]

        # Find the brighest RGB palette component for normalization
        if self._normalize:
            self._ref_palette_max = numpy.max(self._ref_palette)
        else:
            self._ref_palette_max = 0xFF
        self._new_palette = self.fade_normalize()

    @property
    def brightness(self):
        """The palette's overall brightness level, 0.0 to 1.0."""
        return self._brightness

    @brightness.setter
    def brightness(self, new_brightness):
        if new_brightness != self._brightness:
            self._brightness = new_brightness
            self._new_palette = self.fade_normalize()

    @property
    def gamma(self):
        """The adjusted palette's gamma value, typically from 0.0 to 2.0. The
        gamma adjustment is applied after the palette is normalized and
        brightness-adjusted."""
        return self._gamma

    @property
    def normalize(self):
        """The palette's normalization mode state; True to normalize."""
        return self._normalize

    @property
    def palette(self):
        """The adjusted displayio palette."""
        return self._new_palette

    def fade_normalize(self):
        """Create an adjusted displayio palette from the reference palette. Use
        the current brightness, gamma, and normalize parameters to build the
        adjusted palette. The reference palette is first adjusted for
        brightness and normalization (if enabled), followed by the gamma
        adjustment. Transparency index values are preserved."""
        # Determine the normalization factor to apply to the palette
        self._norm_factor = round((0xFF / self._ref_palette_max) * self._brightness, 3)

        # If needed, normalize from the reference palette
        if self._norm_factor != 1.000 or self._gamma != 1.0:
            self._new_palette = self._src_palette  # Preserves transparency values
            norm_palette = numpy.array(
                self._ref_palette * self._norm_factor, dtype=numpy.uint8
            )
            norm_palette = numpy.array(norm_palette**self._gamma, dtype=numpy.uint8)

            # Build new_palette with the newly normalized changes
            for i, color in enumerate(norm_palette):
                self._new_palette[i] = (
                    (norm_palette[i, 0] << 16)
                    + (norm_palette[i, 1] << 8)
                    + norm_palette[i, 2]
                )
        return self._new_palette


def set_color_brightness(self, source_color, brightness=1.0, gamma=1.0):
    """Scale a 24-bit RGB source color value in proportion to the brightness
    setting (0 to 1.0). Returns an adjusted 24-bit RGB color value or None if
    the source color is None (transparent). The adjusted color's gamma value is
    typically from 0.0 to 2.0 with a default of 1.0 for no gamma adjustment."""

    if source_color is None:
        return

    # Extract primary colors and scale to brightness
    r = min(int(brightness * ((source_color & 0xFF0000) >> 16)), 0xFF)
    g = min(int(brightness * ((source_color & 0x00FF00) >> 8)), 0xFF)
    b = min(int(brightness * ((source_color & 0x0000FF) >> 0)), 0xFF)

    # Adjust result for gamma perception
    r = min(int(round((r**gamma), 0)), 0xFF)
    g = min(int(round((g**gamma), 0)), 0xFF)
    b = min(int(round((b**gamma), 0)), 0xFF)

    return (r << 16) + (g << 8) + b
