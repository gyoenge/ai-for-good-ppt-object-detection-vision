# %%
from PIL import Image
import numpy as np
import json

def get_dominant_colors(image_path):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    pixels = img.getdata()

    color_counts = {}
    for pixel in pixels:
        color = tuple(pixel)
        if color in color_counts:
            color_counts[color] += 1
        else:
            color_counts[color] = 1

    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)

    dominant_colors = []
    for color in sorted_colors:
        if color[1] < 800:
            break
        if color[0] != (255, 255, 255):
            dominant_colors.append(color[0])

    print(dominant_colors)
    return dominant_colors

def center_of_gravity(arr):

  if len(arr.shape) == 2:
    # Grayscale image
    y, x = np.ogrid[:arr.shape[0], :arr.shape[1]]
    weights = arr.astype(float)
  elif len(arr.shape) == 3:
    # Color image (assuming RGB)
    y, x = np.ogrid[:arr.shape[0], :arr.shape[1]]
    weights = arr.mean(axis=2).astype(float)  # Average across color channels
  else:
    raise ValueError("Input array must be a 2D or 3D NumPy array.")

  # Calculate center of gravity coordinates
  cog_x = np.sum(weights * x) / np.sum(weights)
  cog_y = np.sum(weights * y) / np.sum(weights)

  return (cog_x, cog_y)

def get_cgs(image_path, colors):
    img = Image.open(image_path)
    img_array = np.array(img)

    filtered_imgs = []

    for color in colors:
        filtered_imgs.append((img_array == [color[0], color[1], color[2]]).all(axis=2))
    
    for i in range(len(filtered_imgs)):
        img = Image.fromarray(filtered_imgs[i])
        img.save(f'{i}.jpg')

    cgs = []
    for filtered_img in filtered_imgs:
        cgs.append(center_of_gravity(filtered_img))

    return cgs

def get_rasterized_line(point_a, point_b, image_path):
  img = np.array(Image.open(image_path).convert('L'))
  image_shape = img.shape

  x_a, y_a = point_a
  x_b, y_b = point_b
  rows, cols = image_shape

  if x_a == x_b:
    return np.full((rows, cols), 0).astype(int)[:, x_a]
  elif y_a == y_b:
    return np.full((rows, cols), 0).astype(int)[y_a, :]

  m = (y_b - y_a) / (x_b - x_a)
  c = y_a - m * x_a

  line_image = np.zeros(image_shape, dtype=int)

  for x in range(cols):
    y = int(m * x + c)
    if 0 <= y < rows:
      line_image[y, x] = 1

  return line_image


# %%
dominant_colors = get_dominant_colors("test.png")
cgs = get_cgs('test.png', dominant_colors)

lines = []
for i in range(len(cgs)):
   for j in range(i+1, len(cgs)):
      lines.append((i, j, get_rasterized_line(cgs[i], cgs[j], "test.png")))

for line in lines:
    img = Image.fromarray(line[2]*255)
    img.save(f'line{line[0]}-{line[1]}.png')

quantized_image = np.zeros_like(
   Image.open("test.png").convert('L'), dtype="int32"
)
print(quantized_image.shape)
for i in range(len(dominant_colors)):
   img = Image.open(f"{i}.jpg").convert('L')
   quantized_image += np.where(np.array(img) > 254, 1, 0) * (i+1)
Image.fromarray(quantized_image*100).save('mix.png')
with open("x.json", "w") as f:
    json.dump(quantized_image.tolist(), f, indent=2)

for line in lines:
   print(line[0], line[1], set(np.multiply(quantized_image, line[2]).flatten()))
