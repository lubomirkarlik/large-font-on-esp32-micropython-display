
# Large Digit Display for LVGL (ESP32 / MicroPython)

This project enables displaying large digits using bitmap fonts with the [LVGL](https://lvgl.io/) graphics library, suitable for embedded devices like the ESP32 with a display (e.g., 5" Elecrow LCD).

![Screenshot](screenshot.png)

## 📦 Project Contents

- `large_fonts.py` – Library for managing and rendering bitmap digits with zoom support.
- `large_digits.py` – Main application script that initializes the display, creates four digit displays, and shows sample values.
- `*.bmp` files – Bitmap images for each digit and symbol (`0`–`9`, `,`, `V`, `A`).
- `snapshot.py` – Optional module for saving LVGL screen snapshots.

## ⚙️ Features

- Display of four numeric values in the format `12.34 V` or `56.78 A`.
- Each digit is rendered using a bitmap image instead of a standard font.
- Full zoom support: scale digits from 0% to undefined %.
- Decimal point and unit symbols are displayed using separate images.
- Screen snapshot functionality (`screenshot.bmp`).

## 🚀 Getting Started

1. Copy all `.py` files and `.bmp` images to your MicroPython device with LVGL support (e.g., ESP32-S3).
2. Run the main script:

```python
import large_digits
```

3. The screen will show four displays with different values and zoom levels.

## 🧠 Requirements

- [LVGL for MicroPython](https://github.com/lvgl/lv_binding_micropython)
- A compatible display (e.g., Elecrow 5" DIS07050H) - tested
- MicroPython build with support for `lvgl`, `framebuf`, `os`, `gc`

## 🖼️ BMP Image Format

- 24-bit BMP format
- RGB converted to RGB565 for display compatibility
- Digit size and design can be customized using image editors (e.g., GIMP)

## 🛠️ Customization

- Spacing, units, and zoom can be adjusted via parameters in the `DigitDisplay` class.
- Additional characters can be added by extending the `digit_files` dictionary in `large_fonts.py` and providing matching `.bmp` images.

## 🧪 Example Output Values

| Position       | Value | Unit | Zoom  |
|----------------|-------|------|-------|
| Top Left       | 12.34 | V    | 200%  |
| Top Right      | 56.78 | V    | 100%  |
| Bottom Left    | 90.12 | A    | 50%   |
| Bottom Right   | 34.56 | A    | 25%   |

## 📄 Libraray documentation

- description of classes, functions, attributes is decribed in large_fonts_doc.md file.

## 📄 License

This project is open-source. You may use and modify it freely. Provide your own bitmap images for custom fonts or symbols.
