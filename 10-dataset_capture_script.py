import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing(240, 240)
sensor.skip_frames(time = 2000)

while(True):
    img = sensor.snapshot()
    img.gamma_corr(gamma=1.75, contrast=1.0, brightness=0.0)
