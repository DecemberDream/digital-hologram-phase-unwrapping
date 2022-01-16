import numpy as np
import imageio
from time import time

def reflection_full(image):
    rows, cols = image.shape

    reflected = np.empty((2 * rows, 2 * cols))
    upper = np.empty((rows, cols * 2))

    upper[:, 0:cols] = image
    upper[:, cols:] = image[:, -1::-1]

    reflected[:rows, :] = upper
    reflected[rows:, :] = upper[-1::-1, :]

    return reflected


def correct_interval(values):
    for i in range(len(values)):
        while True:
            if values[i] <= -PI:
                values[i] += (2 * PI)
            elif values[i] > PI:
                values[i] -= (2 * PI)
            else:
                break

    return values


def row_diff(psi):
    rows, cols = psi.shape

    row_diff = np.zeros((rows, cols))

    for row in range(rows - 1):
        row_diff[row, :] = correct_interval(psi[row + 1, :] - psi[row, :])

    return row_diff


def col_diff(psi):   
    rows, cols = psi.shape

    col_diff = np.zeros((rows, cols))

    for col in range(rows - 1):
        col_diff[:, col] = correct_interval(psi[:, col + 1] - psi[:, col])

    return col_diff


def rho(row_diff, col_diff):
    rows = len(row_diff)
    cols = len(col_diff[0])

    rho = np.empty((rows, cols))

    for row in range(rows):
        for col in range(cols):
            rho[row, col] = row_diff[row, col] - row_diff[row - 1, col] + col_diff[row, col] - col_diff[row, col - 1]
    
    return rho


def kernel(n):
    kernel = np.zeros((n,n), dtype=np.float64)
    kernel[n//2, n//2] = -4
    kernel[n//2 + 1, n//2] = 1
    kernel[n//2 - 1, n//2] = 1
    kernel[n//2, n//2 + 1] = 1
    kernel[n//2, n//2 - 1] = 1
    
    return kernel


def replace_kernel(image_fft):
    k = kernel(len(image_fft))
    k = np.fft.fft2(k)
    k = np.real(k)
    k[0, 0] = 1
    phi = image_fft / k
    phi[0, 0] = 0

    return phi


def replace_func(image_fft):
    rows = len(image_fft)
    cols = len(image_fft[0])

    denominator = np.empty((rows, cols), dtype=np.float64)

    for row in range(rows):
        for col in range(cols):
            denominator[row, col] = (2 * np.cos(PI * row / (rows//2)) + 2 * np.cos(PI * col / (cols//2)) - 4)

    denominator[0, 0] = 1
    phi = image_fft / denominator
    phi[0, 0] = 0

    return phi


t0 = time()
PI = np.pi

file = "test.bmp"

file = file.split(".")
file_name = file[0]
file_ext = file[1]

img = np.float64(imageio.imread(f"input/{file_name}.{file_ext}"))
img = np.fft.fftshift(img)

rows = len(img)
cols = len(img[0])

img = np.interp(img, [0, 255], [-PI, PI])

# Step 1
reflected = reflection_full(img)

row_diffs = row_diff(reflected)
col_diffs = col_diff(reflected)

rho = rho(row_diffs, col_diffs)

# Step 2
image_fft = np.fft.fft2(rho)

# Step 3
replaced = replace_kernel(image_fft)
# replaced = replace_func(image_fft)

# step 4
phi = np.fft.ifftshift(np.fft.ifft2(replaced))[:rows, :cols]
phi = np.real(phi)

# Wrap back properly and turn values into 8-bit integers
phi = phi - np.min(phi)
phi = phi % (2 * PI)
phi = phi / np.max(phi) * 255
phi = np.rint(phi)
phi = np.uint8(phi)

imageio.imsave(f"output/{file_name}_phi.{file_ext}", phi)