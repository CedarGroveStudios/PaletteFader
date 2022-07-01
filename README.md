# CedarGrove PaletteFader

### _A work-in-progress CircuitPython color list and displayio palette brightness setter and normalizer tool._

## Overview

Due to the lack of hardware support for display brightness, the PaletteFader class was developed for controlling the RGB LED matrix panel display attached to an Adafruit MatrixPortal. Although not tested on other devices, the class is expected to be compatible with any displayio graphics application.

Since PaletteFader adjusts brightness by recalculating displayio color values rather than directly controlling brightness in the hardware, it can be somewhat complicated to incorporate into CircuitPython code. Use with bitmap images and spritesheets is fairly straightforward. Other displayio objects such as shapes and labels requires that a color list be created and managed. Due to limitations of certain displayio object color modules, color parameters such as outlines cannot be managed with this tool; only displayio object color and fill parameters are supported at this time.

See the _palettefader_simpletest.py_ in the _examples_ folder for PaletteFader usage.

Creation of this class is also intended to be a CircuitPython-based proof-of-concept to inspire the development of a similar algorithm deep within the confines of the displayio core module. Stay tuned to this channel to see if the plot takes a turn in that direction.

### CedarGrove PaletteFader API Class Description:
https://github.com/CedarGroveStudios/PaletteFader/blob/main/docs/pseudo%20readthedocs%20cedargrove_palettefader.pdf

![Overview](https://github.com/CedarGroveStudios/PaletteFader/blob/main/docs/PaletteFader_Class_description.jpeg)

![Internals](https://github.com/CedarGroveStudios/PaletteFader/blob/main/docs/PaletteFader_Class_internals.jpeg)

### Matrix Weather Project example:
https://github.com/CedarGroveStudios/Matrix_Weather

![MatrixWeather](https://github.com/CedarGroveStudios/Matrix_Weather/blob/main/photos_and_graphics/matrix_weather.jpeg)


### Snowman Project example:
https://github.com/CedarGroveStudios/Matrix_Portal_Snowman

![MatrixPortal Snowman](https://github.com/CedarGroveStudios/Matrix_Portal_Snowman/blob/main/graphics_source/MatrixPortal_Snowman.png)

