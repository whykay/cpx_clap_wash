#
# Modified https://learn.adafruit.com/sensor-plotting-with-mu-and-circuitpython/sound
#

import array, math, time
import audiobusio, board, neopixel

PEAK_COLOR = (100, 0, 255)
NUM_PIXELS = 10

# Exponential scaling factor.
# Should probably be in range -10 .. 10 to be reasonable.
CURVE = 2
SCALE_EXPONENT = math.pow(10, CURVE * -0.1)

# Number of samples to read at once.
NUM_SAMPLES = 160

#cpx.pixels.brightness = 0.1
#init_cnt = 0

# Restrict value to be between floor and ceiling.
def constrain(value, floor, ceiling):
    return max(floor, min(value, ceiling))


# Scale input_value between output_min and output_max, exponentially.
def log_scale(input_value, input_min, input_max, output_min, output_max):
    normalized_input_value = (input_value - input_min) / \
                             (input_max - input_min)
    return output_min + \
        math.pow(normalized_input_value, SCALE_EXPONENT) \
        * (output_max - output_min)


# Remove DC bias before computing RMS.
def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))


def mean(values):
    return sum(values) / len(values)


def volume_color(volume):
    return 200, volume * (255 // NUM_PIXELS), 0

def start_it():
    for l in range(NUM_PIXELS):
        pixels[l] = PEAK_COLOR
    pixels.show()
    time.sleep(1)

def countdown():
    print("In Countdown")
    for i in range(9, -1, -1):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(1)

    pixels.fill((255, 255, 0))
    pixels.show()

    for i in range(NUM_PIXELS):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(1)

# Set up NeoPixels and turn them all off.
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.1, auto_write=False)
pixels.fill(0)
pixels.show()

mic = audiobusio.PDMIn(board.MICROPHONE_CLOCK, board.MICROPHONE_DATA, sample_rate=16000, bit_depth=16)

# Record an initial sample to calibrate. Assume it's quiet when we start.
samples = array.array('H', [0] * NUM_SAMPLES)
mic.record(samples, len(samples))

# Set lowest level to expect, plus a little.
input_floor = normalized_rms(samples) + 10

# You might want to print the input_floor to help adjust other values.
print(input_floor)

# Corresponds to sensitivity: lower means more pixels light up with lower sound
# Adjust this as you see fit.
input_ceiling = input_floor + 500


peak = 0
magnitude = 0
while True:
    mic.record(samples, len(samples))
    magnitude = normalized_rms(samples)
    # You might want to print this to see the values.
    print(magnitude)

    # Light up pixels that are below the scaled and interpolated magnitude.

    if magnitude > 1500:
        pixels.fill(0)
        print(f"I HEARD YOU!: {magnitude}")

        start_it()

        pixels.fill((255, 255, 0))
        pixels.show()
        time.sleep(1)

        start_it()

        pixels.fill((255, 255, 0))
        pixels.show()
        time.sleep(1)

        start_it()

        pixels.fill((255, 255, 0))
        pixels.show()
        time.sleep(0.5)

        # 10 seconds countdown
        countdown()
        magnitude = 0
    else:
        pixels.fill((0, 255, 0))
        pixels.show()
        magnitude = 0



    """
    # Compute scaled logarithmic reading in the range 0 to NUM_PIXELS
    c = log_scale(constrain(magnitude, input_floor, input_ceiling),
                  input_floor, input_ceiling, 0, NUM_PIXELS)

    for i in range(NUM_PIXELS):
        if i < c:
            pixels[i] = volume_color(i)
        # Light up the peak pixel and animate it slowly dropping.
        if c >= peak:
            peak = min(c, NUM_PIXELS - 1)
        elif peak > 0:
            peak = peak - 1
        if peak > 0:
            pixels[int(peak)] = PEAK_COLOR
    """

