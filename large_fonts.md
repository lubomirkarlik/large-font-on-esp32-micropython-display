# Documentation for `large_fonts.py` Library

## Introduction
The `large_fonts.py` library provides tools for displaying large digits on screens using bitmap images. It's designed for use with the LVGL library and allows smooth resizing of displayed digits using zoom functionality.

## `DisplayManager` Class

### Description
Base class for display and screen management.

### Attributes
- `WIDTH` (int): Display width in pixels (default 800)
- `HEIGHT` (int): Display height in pixels (default 480)
- `current_screen` (lv.obj): Reference to currently displayed screen

### Methods

#### `create_screen(bg_color=lv.color_hex(0x000000))`
Creates a new screen with given background color.

**Parameters:**
- `bg_color`: Background color (default black)

**Returns:**
- `lv.obj`: Created screen object

#### `show_screen(screen)`
Displays the specified screen.

**Parameters:**
- `screen`: Screen object to display

## `DigitDisplay` Class

### Description
Class for displaying large digits with zoom capability and decimal point.

### Attributes
- `img_pool` (dict): Pool of images for digits
- `current_screen` (lv.obj): Parent screen
- `x_pos`, `y_pos` (int): Display position
- `base_digit_spacing` (int): Base digit spacing at 100% zoom (255)
- `base_comma_offset` (int): Base decimal point offset at 100% zoom
- `base_suffix_offset` (int): Base suffix offset at 100% zoom
- `max_digits` (int): Maximum number of digits (default 4)
- `img_usage` (dict): Image usage tracking
- `suffix` (str): Display suffix (e.g. 'V', 'A')
- `zoom` (int): Current zoom value (255 = 100%)
- `digit_spacing` (int): Current digit spacing (calculated from zoom)
- `comma_offset` (int): Current decimal point offset
- `suffix_offset` (int): Current suffix offset

### Methods

#### `init_digits(screen)`
Initializes the display with given parent screen.

**Parameters:**
- `screen`: Parent screen object

#### `display_value(int_part, frac_part)`
Displays a numeric value with decimal point.

**Parameters:**
- `int_part`: Integer part (2 digits)
- `frac_part`: Fractional part (2 digits)

#### `set_zoom(zoom_factor)`
Sets zoom scale for all digits.

**Parameters:**
- `zoom_factor`: Zoom value (255 = 100%, 128 = 50%)

#### `_update_spacing()`
Internal method for recalculating spacing based on current zoom.

#### `_load_bmp(filename)`
Loads BMP image from file.

**Parameters:**
- `filename`: Filename to load

**Returns:**
- `lv.img` or `None` on error

#### `_load_digit_images()`
Loads all required digit images into pool.

#### `_get_next_img(digit)`
Gets next available image for given digit from pool.

**Parameters:**
- `digit`: Digit character ('0'-'9', ',')

**Returns:**
- `lv.img` or `None` if not available

## Functions

### `create_4_digit_displays(dm, screen, zoom=255)`
Creates 4 digit displays (2 for voltage, 2 for current) with given zoom scale.

**Parameters:**
- `dm`: `DisplayManager` instance
- `screen`: Target screen
- `zoom`: Initial zoom value (default 255 = 100%)

**Returns:**
- `list`: List of 4 `DigitDisplay` instances

### `refresh_digit_displays(digit_displays, num1, num2, num3, num4)`
Updates all 4 displays with new values.

**Parameters:**
- `digit_displays`: List of displays from `create_4_digit_displays`
- `num1`, `num2`, `num3`, `num4`: New values for displays (as integers, e.g. 1234 = 12.34)

**Returns:**
- `list`: List of values in format `[(int_part, frac_part), ...]`

## Usage Example

```python
import large_fonts
import lvgl as lv

# Initialization
dm = large_fonts.DisplayManager()
screen = dm.create_screen()
dm.show_screen(screen)

# Create displays with 150% zoom
displays = large_fonts.create_4_digit_displays(dm, screen, zoom=382)

# Display values
large_fonts.refresh_digit_displays(displays, 1234, 5678, 9012, 3456)

# Change zoom
for disp in displays:
    disp.set_zoom(200)  # ~80% of original size
