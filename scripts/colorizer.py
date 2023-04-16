from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def colorize(img_url, cmap):
    img = Image.open(img_url)
    color_map = plt.get_cmap(cmap)
    img_data = img.convert('L')
    img_data = np.array(img_data)
    img_data = color_map(img_data)
    img_data = np.uint8(img_data * 255)
    img_colorized = Image.fromarray(img_data)
    img_colorized.save(img_url.rsplit('/', 1)[1].rsplit('.')[0] + cmap + '.png')


cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

for color in cmaps:
    colorize('../data/4.jpg', color)

