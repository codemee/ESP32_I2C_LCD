# 匯入必要的函式庫
from machine import Pin, I2C  # 匯入 MicroPython 的 Pin 和 I2C 控制函式
from i2c_lcd import I2cLcd    # 匯入自定義的 I2C LCD 驅動程式

# 建立 I2C 物件
# SCL 接 GPIO22, SDA 接 GPIO21
i2c = I2C(scl=Pin(22), sda=Pin(21))

# 建立 LCD 物件
# 參數: I2C物件, I2C位址(0x27), 列數(2), 行數(16)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# 清除 LCD 螢幕
lcd.clear()

# 在第一行(預設位置)顯示 "hello"
lcd.putstr("hello")

# 移動游標到第二行的第一個位置 (列1, 行0)
lcd.move_to(1, 0)

# 在第二行顯示 "world"
lcd.putstr('world')
