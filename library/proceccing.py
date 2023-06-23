import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PyQt5.QtGui import QImage, QPixmap


class ROI:
    def __init__(self, x: int, y: int, r: int):
        self.x = x
        self.y = y
        self.r = r

    def measure(self, img: np.ndarray) -> float:
        xs, ys = np.indices(img.shape)
        mask = (xs - self.x) ** 2 + (ys - self.y) ** 2 <= self.r ** 2
        return np.mean(img[mask])

    def get_info(self) -> list:
        return [self.x, self.y, self.r]


def open_image(url) -> np.ndarray:
    return np.array(Image.open(url).convert('L'))


def make_graph(data, f0, name="Example") -> str:
    fig, ax = plt.subplots(figsize=(5, 5))
    data = np.array(data)

    for i in range(len(data[0])):
        data[:, i] = data[:, i] / f0[i]

    for i in range(len(data[0])):
        ax.plot(data[:, i], label=f'Region {i + 1}', linewidth=2)

    # Customize the appearance of the plot
    ax.set_xlabel('Frames', fontsize=12)  # Set the x-axis label and font size
    ax.set_ylabel('Relative Fluorescence', fontsize=12)  # Set the y-axis label and font size
    ax.legend(fontsize=10)  # Set the legend font size

    # Adjust the plot main_layout
    fig.tight_layout()

    # Show the plot
    url = f"graphics/{name}.png"
    plt.savefig(url, dpi=100)
    return url


def colorize(pixmap, cmap) -> QPixmap:
    pil_image = Image.fromqimage(pixmap.toImage())
    img_array = np.array(pil_image.convert('L'))

    color_map = plt.get_cmap(cmap)
    colorized_array = color_map(img_array)

    # Scale array values to 0-255 and convert to uint8
    colorized_array = (colorized_array * 255).astype(np.uint8)

    # Create PIL Image from numpy array
    colorized_img = Image.fromarray(colorized_array)

    image_data = colorized_img.convert("RGBA").tobytes()
    qimage = QImage(image_data, colorized_img.size[0], colorized_img.size[1], QImage.Format_RGBA8888)

    return QPixmap.fromImage(qimage)