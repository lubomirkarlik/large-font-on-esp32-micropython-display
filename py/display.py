import lvgl as lv
import lv_utils
import gt911
from machine import I2C, Pin, reset
import tft_config
import fs_driver


WIDTH = 800
HEIGHT = 480

class Display:
    def __init__(self):
        self.tft = None
        self.tp = None
        self.disp = None
        self.indev = None
        self.scr = None
        
    def initialize(self):
        """Initialize display and touch panel"""
        try:
            # Initialize TFT display
            self._init_display()
            
            # Initialize touch panel
            self._init_touch()
            
            # Initialize LVGL
            self._init_lvgl()
            
            # Create main screen
            self.scr = lv.scr_act()
            self.scr.clean()
            self.scr.set_style_bg_color(lv.palette_main(lv.PALETTE.NONE), 0)

            return True
            
        except Exception as e:
            print("Display initialization failed:", e)
            reset()
    
    def _init_display(self):
        """Initialize TFT display hardware"""
        try:
            self.tft = tft_config.config()
        except Exception as e:
            print("TFT initialization error:", e)
            reset()
            raise
    
    def _init_touch(self):
        """Initialize touch panel"""
        i2c = I2C(1, scl=Pin(20), sda=Pin(19), freq=400000)
        self.tp = gt911.GT911(i2c, width=WIDTH, height=HEIGHT)
#        self.tp.set_rotation(self.tp.ROTATION_NORMAL)
        self.tp.set_rotation(self.tp.ROTATION_INVERTED)
    
    def _init_lvgl(self):
        """Initialize LVGL graphics library"""
        lv.init()
        
        # Start event loop if not running
        if not lv_utils.event_loop.is_running():
            event_loop = lv_utils.event_loop()
            print("LVGL Event loop running:", event_loop.is_running())
        
        # Initialize display buffer
        self._init_display_buffer()
        
        # Initialize filesystem driver
        fs_drv = lv.fs_drv_t()
        fs_driver.fs_register(fs_drv, 'S')
    
    def _init_display_buffer(self):
        """Initialize display buffer for LVGL"""
        disp_buf = lv.disp_draw_buf_t()
        buf = bytearray(WIDTH * 50)  # 50 lines buffer
        disp_buf.init(buf, None, len(buf) // lv.color_t.__SIZE__)
        
        # Register display driver
        disp_drv = lv.disp_drv_t()
        disp_drv.init()
        disp_drv.draw_buf = disp_buf
        disp_drv.flush_cb = self.tft.flush
        disp_drv.hor_res = WIDTH
        disp_drv.ver_res = HEIGHT
        self.disp = disp_drv.register()
        lv.disp_t.set_default(self.disp)
        
        # Register touch driver
        indev_drv = lv.indev_drv_t()
        indev_drv.init()
        indev_drv.disp = self.disp
        indev_drv.type = lv.INDEV_TYPE.POINTER
        indev_drv.read_cb = self.tp.lvgl_read
        self.indev = indev_drv.register()
    
    def get_screen(self):
        """Get the main screen object"""
        return self.scr or lv.scr_act()
    
    def get_touch_point(self):
        """Get current touch point coordinates"""
        return self.tp.get_point() if self.tp else None

# Singleton display instance
display = Display()

def init():
    """Initialize the display (convenience function)"""
    return display.initialize()