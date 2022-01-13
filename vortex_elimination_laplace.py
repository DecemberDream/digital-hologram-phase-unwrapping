import numpy as np
import imageio


def reflection_full(image):
    rows = len(image)
    cols = len(image[0])

    reflected = np.empty((2 * rows, 2 * cols))
    upper = np.empty((rows, cols * 2))

    upper[:, 0:cols] = image
    upper[:, cols:] = image[:, -1::-1]

    reflected[:rows, :] = upper
    reflected[rows:, :] = upper[-1::-1, :]

    return reflected


PI = np.pi
cos = np.cos

img = np.float64(imageio.imread("input/test.bmp"))
img = np.fft.fftshift(img)

rows = len(img)
cols = len(img[0])

img = np.interp(img, [0, 255], [-PI, PI])

# Step 1
reflected = reflection_full(img)