import numpy as np
import imageio
import matplotlib.pyplot as plt


def generate_anti_vortices(h, w):
    pos_curl = np.empty((2 * h, 2 * w), dtype=np.float64)
    neg_curl = np.empty((2 * h, 2 * w), dtype=np.float64)
    
    for row in range(2 * h):
        for col in range(2 * w):
            pos_curl[row, col] = np.arctan2(h - (row + .5), (col + .5) - w)
            neg_curl[row, col] = np.arctan2(h - (row + .5), w - (col + .5))
            
    return neg_curl, pos_curl


PI = np.pi

file = "test.bmp"

file = file.split(".")
file_name = file[0]
file_ext = file[1]

img_original = np.float64(imageio.imread(f"input/{file_name}.{file_ext}"))

img = img_original / 255 * 2 * PI

height, width = img.shape

# Copy first row and column to end of image
img_ext = np.empty((height + 1, width + 1), dtype=img.dtype)
img_ext[0:-1, 0:-1] = img  # copy image
img_ext[0:-1, -1] = img[:, 0]  # copy first column
img_ext[-1, :] = img_ext[0, :]

img_to_clear = np.copy(img)

found_vortices = np.full_like(img, 128)

# Generate anti-vortex
anti_vortex_right, anti_vortex_left = generate_anti_vortices(height, width)

plt.imshow(anti_vortex_left)
plt.show()


        