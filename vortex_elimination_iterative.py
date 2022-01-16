import numpy as np
import imageio


def generate_anti_vortices(h, w):
    pos_curl = np.empty((2 * h, 2 * w), dtype=np.float64)
    neg_curl = np.empty((2 * h, 2 * w), dtype=np.float64)
    
    for row in range(2 * h):
        for col in range(2 * w):
            pos_curl[row, col] = np.arctan2(h - (row + .5), (col + .5) - w)
            neg_curl[row, col] = np.arctan2(h - (row + .5), w - (col + .5))
            
    return neg_curl, pos_curl


# Bring value/image into interval [-PI, PI]
def wrap(a):
    return (a + PI) % (2 * PI) - PI
    

# Epsilon accounts for numerical inaccuracies
def is_2_pi(value, epsilon=0.0000001):
    return 2 * PI - epsilon <= value <= 2 * PI + epsilon


def get_vortex_type(m):
    # Calculate differences clockwise
    diff_1 = wrap(m[0, 1] - m[0, 0])
    diff_2 = wrap(m[1, 1] - m[0, 1])
    diff_3 = wrap(m[1, 0] - m[1, 1])
    diff_4 = wrap(m[0, 0] - m[1, 0])
    
    diff_sum = diff_1 + diff_2 + diff_3 + diff_4
    
    if is_2_pi(diff_sum):
        return 1
    elif is_2_pi(-diff_sum):
        return -1
    else:
        return 0


PI = np.pi

file = "test.bmp"

file = file.split(".")
file_name = file[0]
file_ext = file[1]

img_original = np.float64(imageio.imread(f"input/{file_name}.{file_ext}"))

# Bring image into interval [0, 2PI]
img = img_original / 255 * 2 * PI

rows, cols = img.shape

# Copy first row and column to end of image
img_ext = np.empty((rows + 1, cols + 1), dtype=img.dtype)
img_ext[0:-1, 0:-1] = img  # copy image
img_ext[0:-1, -1] = img[:, 0]  # copy first column
img_ext[-1, :] = img_ext[0, :]

# To visualize origins of vortices
found_vortices = np.full_like(img, 128, dtype=np.uint8)

# Generate anti-vortex
anti_vortex_neg, anti_vortex_pos = generate_anti_vortices(rows, cols)

vortex_center_y = rows - 1
vortex_center_x = cols - 1

num_of_vortices = 0

for row in range(rows):
    for col in range(cols):
        four_pixel_matrix = img_ext[row:row + 2, col:col + 2]
        vortex_type = get_vortex_type(four_pixel_matrix)
        
        if vortex_type != 0:
            num_of_vortices += 1
            
            # Calculate coordinates of vortex snippet
            vortex_coord_start_y = vortex_center_y - row
            vortex_coord_end_y = vortex_center_y + (rows - row)
            vortex_coord_start_x = vortex_center_x - col
            vortex_coord_end_x = vortex_center_x + (cols - col)
            
            anti_vortex_snippet = np.empty_like(img)
            
            if vortex_type == 1:
                found_vortices[row, col] = 0
                anti_vortex_snippet = anti_vortex_pos[vortex_coord_start_y:vortex_coord_end_y,
                                                       vortex_coord_start_x:vortex_coord_end_x]
                
            else:
                found_vortices[row, col] = 255
                anti_vortex_snippet = anti_vortex_neg[vortex_coord_start_y:vortex_coord_end_y,
                                                       vortex_coord_start_x:vortex_coord_end_x]
                
            img += anti_vortex_snippet

img_clean = wrap(img)

# Wrap back properly and turn values into 8-bit integers
img_clean = img_clean - np.min(img_clean)
img_clean = img_clean % (2 * PI)
img_clean = img_clean / np.max(img_clean) * 255
img_clean = np.rint(img_clean)
img_clean = np.uint8(img_clean)

imageio.imsave(f"output/{file_name}_it.{file_ext}", img_clean)

if num_of_vortices > 0:
    imageio.imsave(f"output/{file_name}_vortex_positions.{file_ext}", found_vortices)