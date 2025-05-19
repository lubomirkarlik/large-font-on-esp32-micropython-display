# large_font.py - Library for large digit displays with zoom capability
import lvgl as lv
import os, gc

class DisplayManager:
    def __init__(self, width=800, height=480):
        self.WIDTH = width
        self.HEIGHT = height
        self.current_screen = None
        
    def create_screen(self, bg_color=lv.color_hex(0x000000)):
        """Create a new screen with optional background color"""
        screen = lv.obj()
        screen.set_size(self.WIDTH, self.HEIGHT)
        screen.set_style_bg_color(bg_color, lv.PART.MAIN)
        return screen
    
    def show_screen(self, screen):
        """Display the specified screen"""
        screen.set_parent(lv.scr_act())
        self.current_screen = screen
        lv.scr_load(screen)

class DigitDisplay:
    def __init__(self, display_manager, x_pos, y_pos, suffix=None, zoom=128):
        self.dm = display_manager
        self.img_pool = {}  # Image pool for all digits
        self.current_screen = None
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.base_digit_spacing = 50  # Základný rozostup pri zoom=255 (100%)
        self.base_comma_offset = 25   # Základný offset desatinnej čiarky pri zoom=255
        self.base_suffix_offset = 5   # Základný offset sufixu pri zoom=255
        self.max_digits = 4  # For 4-digit display
        self.img_usage = {}
        self.suffix = suffix
        self.zoom = zoom  # Zoom factor (255 = 100%, 128 = 50%)
        # Vypočítame aktuálne rozostupy podľa zoomu
        self._update_spacing()
        
    def init_digits(self, screen):
        """Initialize display with parent screen"""
        self.current_screen = screen
        self._load_digit_images()
        
    def _load_bmp(self, filename):
        """Load BMP image from file"""
        try:
            with open(filename, 'rb') as f:
                data = f.read()

            if data[0:2] != b'BM':
                raise ValueError("Not a valid BMP file")

            width = int.from_bytes(data[18:22], 'little')
            height = int.from_bytes(data[22:26], 'little')
            bpp = int.from_bytes(data[28:30], 'little')
            data_offset = int.from_bytes(data[10:14], 'little')

            if bpp != 24:
                raise ValueError("Only 24-bit BMP supported")

            row_padding = (4 - (width * 3) % 4) % 4
            img_data = bytearray(width * height * 2)

            for y in range(height):
                for x in range(width):
                    bmp_pos = data_offset + (height - 1 - y) * (width * 3 + row_padding) + x * 3
                    b, g, r = data[bmp_pos], data[bmp_pos+1], data[bmp_pos+2]
                    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                    img_data[(y * width + x) * 2] = rgb565 & 0xFF
                    img_data[(y * width + x) * 2 + 1] = (rgb565 >> 8) & 0xFF

            img_dsc = lv.img_dsc_t({
                'data_size': len(img_data),
                'data': img_data,
                'header': {
                    'w': width,
                    'h': height,
                    'cf': lv.img.CF.TRUE_COLOR
                }
            })

            img = lv.img(self.current_screen)
            img.set_src(img_dsc)
            img.set_pos(-1000, -1000)  # Hide initially
            return img
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None

    def _load_digit_images(self):
        """Load all digit images into pool"""
        digit_files = {
            '0': '30.bmp',
            '1': '31.bmp',
            '2': '32.bmp',
            '3': '33.bmp',
            '4': '34.bmp',
            '5': '35.bmp',
            '6': '36.bmp',
            '7': '37.bmp',
            '8': '38.bmp',
            '9': '39.bmp',
            ',': '2e.bmp',
            'V': 'V.bmp',
            'A': 'A.bmp'
        }

        for digit, filename in digit_files.items():
            self.img_pool[digit] = []
            original_img = self._load_bmp(filename)
            if not original_img:
                print(f"Warning: Failed to load '{digit}' from {filename}")
                continue

            src = original_img.get_src()
            original_img.set_pos(-1000, -1000)
            self.img_pool[digit].append(original_img)

            # Create extra copies for each digit position
            for _ in range(self.max_digits - 1):
                img = lv.img(self.current_screen)
                img.set_src(src)
                img.set_pos(-1000, -1000)
                self.img_pool[digit].append(img)
    
    def _get_next_img(self, digit):
        """Get next available image for digit from pool"""
        if digit not in self.img_usage:
            self.img_usage[digit] = 0
        index = self.img_usage[digit]
        pool = self.img_pool.get(digit, [])
        if index < len(pool):
            img = pool[index]
            self.img_usage[digit] += 1
            return img
        else:
            print(f"Not enough images for digit '{digit}'!")
            return None

    def display_value(self, int_part, frac_part):
        """Display a numeric value with decimal point"""
        str_int = f"{int_part:02d}"  # 2-digit integer part
        str_frac = f"{frac_part:02d}"  # 2-digit fractional part
        all_digits = list(str_int + str_frac)  # Combine all digits
        
        self.img_usage = {}  # Reset image usage tracking
        
        # Pred zobrazením prepočítame rozostupy podľa aktuálneho zoomu
        self._update_spacing()
        
        # Display integer part digits (first 2 digits)
        for i in range(2):
            digit = all_digits[i]
            pos_x = self.x_pos + i * self.digit_spacing
            
            # Hide leading zero
            if i == 0 and digit == '0':
                for other_digit, pool in self.img_pool.items():
                    for other_img in pool:
                        if other_img.get_x() == pos_x:
                            other_img.set_pos(-1000, self.y_pos)
                continue
                
            img = self._get_next_img(digit)
            if img:
                # Hide any other image at this position
                for other_digit, pool in self.img_pool.items():
                    for other_img in pool:
                        if other_img is not img and other_img.get_x() == pos_x:
                            other_img.set_pos(-1000, self.y_pos)
                img.set_pos(pos_x, self.y_pos)
                img.set_zoom(self.zoom)

        # Display decimal comma
        comma_pos_x = self.x_pos + 2 * self.digit_spacing
        comma_img = self._get_next_img(',')
        if comma_img:
            comma_img.set_pos(comma_pos_x, self.y_pos)
            comma_img.set_zoom(self.zoom)

        # Display fractional part digits (last 2 digits)
        for i in range(2, 4):
            digit = all_digits[i]
            pos_x = self.x_pos + (i) * self.digit_spacing + self.comma_offset
            
            img = self._get_next_img(digit)
            if img:
                for other_digit, pool in self.img_pool.items():
                    for other_img in pool:
                        if other_img is not img and other_img.get_x() == pos_x:
                            other_img.set_pos(-1000, self.y_pos)
                img.set_pos(pos_x, self.y_pos)
                img.set_zoom(self.zoom)

        # Display suffix if specified
        if self.suffix in self.img_pool:
            suffix_img = self._get_next_img(self.suffix)
            if suffix_img:
                suffix_x = self.x_pos + 4 * self.digit_spacing + self.comma_offset + self.suffix_offset
                # Nastavenie priamej pozície pre suffix
                suffix_img.set_pos(suffix_x, self.y_pos)
                suffix_img.set_zoom(self.zoom)

    def _update_spacing(self):
        """Prepočíta rozostupy medzi číslicami podľa aktuálneho zoomu"""
        zoom_factor = self.zoom / 255.0  # 255 = 100%, 128 = 50%
        self.digit_spacing = int(self.base_digit_spacing * zoom_factor)
        self.comma_offset = int(self.base_comma_offset * zoom_factor)
        self.suffix_offset = int(self.base_suffix_offset * zoom_factor)
        
    def set_zoom(self, zoom_factor):
        """Set zoom factor for all digits (255 = 100%)"""
        self.zoom = zoom_factor
        self._update_spacing()  # Prepočítame rozostupy po zmene zoomu

def create_4_digit_displays(dm, screen, zoom=255):
    """Create 4 digit displays with specified zoom level (255 = 100%)"""
    digit_displays = []
    positions = [
        (70, 50),  # Top left (V)
        (70, 200),  # Top right (V)
        (70, 300),  # Bottom left (A)
        (70, 370),  # Bottom right (A)
    ]
    suffixes = ['V', 'V', 'A', 'A']

    for (x, y), suffix in zip(positions, suffixes):
        disp = DigitDisplay(dm, x, y, suffix=suffix)
        disp.set_zoom(zoom)
        disp.init_digits(screen)
        digit_displays.append(disp)

    return digit_displays

def refresh_digit_displays(digit_displays, num1, num2, num3, num4):
    """Refresh all 4 digit displays with new values"""
    values = [
        (num1 // 100, num1 % 100),  # First display (voltage)
        (num2 // 100, num2 % 100),  # Second display (voltage)
        (num3 // 100, num3 % 100),  # Third display (current)
        (num4 // 100, num4 % 100)   # Fourth display (current)
    ]
    
    for disp, (int_p, frac_p) in zip(digit_displays, values):
        disp.display_value(int_p, frac_p)
    
    return values