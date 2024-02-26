from machine import I2C
from vl53l1x import VL53L1X
import time

tof = VL53L1X(I2C(2))

while True:
  distance = tof.read()

  print(distance)
  if distance < 50:
    print("Triggered!")
  time.sleep_ms(50)
