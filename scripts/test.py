from library import proceccing
from PIL import Image
import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)
roi = proceccing.ROI(250, 278, 31)
print(roi.measure(proceccing.open_image("data/HEK_WT_V1_203_stabilized-277.png")))