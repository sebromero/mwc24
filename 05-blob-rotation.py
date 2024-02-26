import sensor, image, time
import math
from utime import sleep_ms

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.
thresholds = (60, 140) # Define the grayscale range we're looking for

def print_blob_info(blob):
    print("Density: ", blob.density())
    print("Pixels: ", blob.pixels())
    print("Area: ", blob.area())
    print("Width: ", blob.w())
    print("Elongation: ", blob.elongation())
    print("Roundness: ", blob.roundness())
    print("-----------------")

while(True):
    clock.tick()                    # Update the FPS clock.
    target_image = sensor.snapshot()         # Take a picture and return the image.
    target_image.gamma_corr(gamma=1.65, contrast=1.75, brightness=0.0)
    #print(clock.fps()) # Note: Runs about half as fast when connected to the IDE

    # Find blobs
    blobs = target_image.find_blobs([thresholds], area_threshold=100*100, merge=True)

    # Draw blobs
    for blob in blobs:
        rotation = blob.rotation_deg()
        if rotation < 160:
           target_image.draw_string(10, 240 - 20,"MISALIGNED!", 128)
        target_image.draw_rectangle(blob.rect(), color=128)
        target_image.draw_cross(blob.cx(), blob.cy(), color=128)
        #print_blob_info(blob)
        print("Rotation:", rotation)
        #print("Corners:", blob.corners())
