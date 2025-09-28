#!/usr/bin/env python3

import sys
import time

import adafruit_ens160
import board

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

ens = adafruit_ens160.ENS160(i2c, 0x52)
ens2 = adafruit_ens160.ENS160(i2c, 0x53)

# Set the temperature compensation variable to the ambient temp
# for best sensor calibration
ens.temperature_compensation = 25
ens2.temperature_compensation = 25
# Same for ambient relative humidity
ens.humidity_compensation = 50
ens2.humidity_compensation = 50

print(f"0x52: AQI (1-5): {ens.AQI}, TVOC (ppb): {ens.TVOC}, eCO2 (ppm): {ens.eCO2}")
print(f"0x53: AQI (1-5): {ens2.AQI}, TVOC (ppb): {ens2.TVOC}, eCO2 (ppm): {ens2.eCO2}")
sys.exit(0)

#

while True:
    print(f"0x52: AQI (1-5): {ens.AQI}, TVOC (ppb): {ens.TVOC}, eCO2 (ppm): {ens.eCO2}")
    print(f"0x53: AQI (1-5): {ens2.AQI}, TVOC (ppb): {ens2.TVOC}, eCO2 (ppm): {ens2.eCO2}")
    print()

    # new data shows up every second or so
    time.sleep(1)