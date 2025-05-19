import lvgl as lv
import display
import large_fonts

display.init()

# Initialize display manager
dm = large_fonts.DisplayManager()

# Create screen
screen = dm.create_screen()
dm.show_screen(screen)

# Create 4 digit displays with different zoom levels
displays = large_fonts.create_4_digit_displays(dm, screen, zoom=128)
displays[0].set_zoom(512)  # 200% zoom
displays[1].set_zoom(255)  # 100% zoom
displays[2].set_zoom(128)  # 50% zoom
displays[3].set_zoom(64)   # 25% zoom

# Update displays with values
large_fonts.refresh_digit_displays(displays, 1234, 5678, 9012, 3456)

import snapshot

snapshot.take_screenshot("/screenshot.bmp")

