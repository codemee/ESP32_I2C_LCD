
from machine import I2C
import time

# PCF8574 default address
DEFAULT_I2C_ADDR = 0x27

# Commands
LCD_CLEAR_DISPLAY = 0x01
LCD_RETURN_HOME = 0x02
LCD_ENTRY_MODE_SET = 0x04
LCD_DISPLAY_CONTROL = 0x08
LCD_CURSOR_SHIFT = 0x10
LCD_FUNCTION_SET = 0x20
LCD_SET_CGRAM_ADDR = 0x40
LCD_SET_DDRAM_ADDR = 0x80

# Flags for entry mode
LCD_ENTRY_RIGHT = 0x00
LCD_ENTRY_LEFT = 0x02
LCD_ENTRY_SHIFT_INCREMENT = 0x01
LCD_ENTRY_SHIFT_DECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAY_ON = 0x04
LCD_DISPLAY_OFF = 0x00
LCD_CURSOR_ON = 0x02
LCD_CURSOR_OFF = 0x00
LCD_BLINK_ON = 0x01
LCD_BLINK_OFF = 0x00

# Flags for function set
LCD_8BIT_MODE = 0x10
LCD_4BIT_MODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Flags for backlight
LCD_BACKLIGHT = 0x08
LCD_NO_BACKLIGHT = 0x00

# Enable bit
En = 0b00000100
# Register select bit
Rs = 0b00000001

class I2cLcd:
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight_val = LCD_BACKLIGHT

        self.display_function = LCD_FUNCTION_SET | LCD_4BIT_MODE | LCD_2LINE | LCD_5x8DOTS
        self.display_control = LCD_DISPLAY_CONTROL | LCD_DISPLAY_ON | LCD_CURSOR_OFF | LCD_BLINK_OFF
        self.display_mode = LCD_ENTRY_MODE_SET | LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT

        # Wait for initialization
        time.sleep_ms(50)
        
        # Send function set command sequence
        self.write_4_bits(0x03 << 4)
        time.sleep_us(4500)
        self.write_4_bits(0x03 << 4)
        time.sleep_us(4500)
        self.write_4_bits(0x03 << 4)
        time.sleep_us(150)
        self.write_4_bits(0x02 << 4)

        # Set function, display control, and entry mode
        self.write_command(self.display_function)
        self.write_command(self.display_control)
        self.write_command(self.display_mode)
        self.clear()

    def write_4_bits(self, data):
        """Writes 4 bits of data to the LCD."""
        self.i2c.writeto(self.i2c_addr, bytes([data | self.backlight_val]))
        self.strobe(data)

    def strobe(self, data):
        """Clocks EN to latch command."""
        self.i2c.writeto(self.i2c_addr, bytes([data | En | self.backlight_val]))
        time.sleep_us(1)
        self.i2c.writeto(self.i2c_addr, bytes([(data & ~En) | self.backlight_val]))
        time.sleep_us(50)

    def write_command(self, cmd):
        """Writes a command to the LCD."""
        # Send high nibble
        self.write_4_bits(cmd & 0xF0)
        # Send low nibble
        self.write_4_bits((cmd << 4) & 0xF0)

    def write_data(self, data):
        """Writes data to the LCD."""
        # Send high nibble
        self.write_4_bits(Rs | (data & 0xF0))
        # Send low nibble
        self.write_4_bits(Rs | ((data << 4) & 0xF0))

    def clear(self):
        """Clears the display."""
        self.write_command(LCD_CLEAR_DISPLAY)
        time.sleep_ms(2)

    def putstr(self, string):
        """Prints a string to the LCD."""
        for char in string:
            self.write_data(ord(char))

    def move_to(self, row, col):
        """Moves the cursor to a specific row and column."""
        addr = col
        if row == 1:
            addr |= 0x40
        self.write_command(LCD_SET_DDRAM_ADDR | addr)

    def backlight_on(self):
        """Turns the backlight on."""
        self.backlight_val = LCD_BACKLIGHT
        self.write_command(0)

    def backlight_off(self):
        """Turns the backlight off."""
        self.backlight_val = LCD_NO_BACKLIGHT
        self.write_command(0)
