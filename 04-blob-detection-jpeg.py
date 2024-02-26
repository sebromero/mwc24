import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True) # Flips the image vertically
sensor.set_hmirror(True) # Mirrors the image horizontally
#sensor.skip_frames(time = 2000)

clock = time.clock()
img = image.Image("/cold-storage-high.jpg", copy_to_fb=True)
img.to_rgb565()

img_org = sensor.alloc_extra_fb(img.width(), img.height(), sensor.RGB565)
img_org.replace(img)

threshold_boxes = (15, 45, 0, 30, -70, -34)
roi = (62, 78, 83, 73)

while(True):
    clock.tick()                    # Update the FPS clock.
    #img = sensor.snapshot()
    img.replace(img_org)

    # Find blobs with a minimal area of 40x5 = 200 px
    # Overlapping blobs will be merged
    blobs = img.find_blobs([threshold_boxes], merge=True, area_threshold=200, roi=roi)

    # Draw blobs
    for blob in blobs:
        # Draw a rectangle where the blob was found
        img.draw_rectangle(blob.rect(), color=(0,255,0))
        # Draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))

    img.draw_string(img.width() - 75, img.height() - 25, f"{len(blobs)} BOXES", scale=2, mono_space=False)

    img.flush()
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    ## to the IDE. The FPS should increase once disconnected.
