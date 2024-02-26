import sensor, image, time, tf, pyb, math
from machine import Pin, SoftI2C
from utime import ticks_ms

min_confidence = 0.5

colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

blueLED = pyb.LED(3) # built-in blue LED
net = None
labels = None
clock = time.clock()                # Create a clock object to track the FPS.
sorted_counts = None

try:
    # Load built in model
    labels, net = tf.load_builtin_model('trained')
except Exception as e:
    raise Exception(e)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
#sensor.set_vflip(True) # Flips the image vertically
#sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time = 2000)     # Wait for settings take effect.


def get_center(detection):
    [x, y, w, h] = detection.rect()
    center_x = math.floor(x + (w / 2))
    center_y = math.floor(y + (h / 2))
    return (center_x, center_y)

def get_distances(detection_list):
    distances = []
    for d in detection_list:
        d_center = get_center(d)
        for o in detection_list:
            if d == o: continue
            o_center = get_center(o)
            distances.append(math.sqrt(pow(o[0] - d[0], 2) + pow(o[1] - d[1], 2)))
    return distances

def get_insect_list(img, distance_threshold = 40):
    global colors

    insects = dict.fromkeys(labels, 0)
    del insects['background']

    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if (i == 0): continue # background class
        if (len(detection_list) == 0): continue # no detections for this class?
        filtered_distances = list(filter(lambda d: (d < distance_threshold), get_distances(detection_list)))
        insects[labels[i]] = len(detection_list) - len(filtered_distances)

        #print("********** %s **********" % labels[i])
        for d in detection_list:
            [x, y, w, h] = d.rect()
            center_x = math.floor(x + (w / 2))
            center_y = math.floor(y + (h / 2))
            #print('x %d\ty %d' % (center_x, center_y))
            img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)
    return insects

def analyze_image(img):
    insects = get_insect_list(img)

    sorted_insects = sorted(insects.items())
    sorted_counts = list(map(lambda x: x[1], sorted_insects))
    print("---------------------------------------")
    print("Insects: %s" % sorted_insects)
    print("---------------------------------------\n")

    return sorted_counts

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    img.gamma_corr(gamma=1.75, contrast=1.0, brightness=0.0)

    sorted_counts = analyze_image(img) # Return value unused in this example

    #print(clock.fps()) # Note: OpenMV Cam runs about half as fast when connected
                         # to the IDE. The FPS should increase once disconnected.
