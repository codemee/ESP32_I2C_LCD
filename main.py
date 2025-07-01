from machine import Pin, I2C
from i2c_lcd import I2cLcd

i2c = I2C(scl=Pin(22), sda=Pin(21))

lcd = I2cLcd(i2c, 0x27, 2, 16)

lcd.clear()
lcd.putstr("hello")
lcd.move_to(1, 0)
lcd.putstr('world')