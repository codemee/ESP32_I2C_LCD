# ESP32 I2C LCD 驅動 (MicroPython)

本專案提供 MicroPython 下 ESP32 使用 PCF8574 I2C LCD 模組的驅動程式及範例程式。

## 檔案結構

- `i2c_lcd.py` : I2C LCD 驅動程式
- `main.py`    : 範例程式，在 LCD 的上下兩行分別顯示 "hello" 與 "world"

## 硬體連接

- ESP32 SDA -> GPIO21
- ESP32 SCL -> GPIO22
- LCD VCC  -> 5V (一定要接 5V)
- LCD GND  -> GND

## 使用方式

1. 將 `i2c_lcd.py` 和 `main.py` 上傳到 ESP32 根目錄。
2. 透過串列埠進入 REPL 或重啟裝置。
3. LCD 分別顯示 "hello" 與 "world" (上下兩行)。

## 調整

- 若 I2C 位址不同，請編輯 `main.py` 中的 `0x27`。
- 若使用其他腳位，可修改 `Pin(21)` / `Pin(22)`。