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
    rows = len(psi)
    cols = len(psi[0])

    row_diff = np.zeros((rows, cols))

    for row in range(rows - 1):
        row_diff[row, :] = correct_interval(psi[row + 1, :] - psi[row, :])

    return row_diff


def col_diff(psi):
    rows = len(psi)
    cols = len(psi[0])

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


PI = np.pi
cos = np.cos

img = np.float64(imageio.imread("input/test.bmp"))
img = np.fft.fftshift(img)

rows = len(img)
cols = len(img[0])

img = np.interp(img, [0, 255], [-PI, PI])

# Step 1
reflected = reflection_full(img)

row_diffs = row_diff(reflected)
col_diffs = col_diff(reflected)

rho = rho(row_diffs, col_diffs)