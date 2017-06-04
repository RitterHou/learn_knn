from PIL import Image
from numpy import *

img = array(Image.open('num/0_5.png'))  # 打开图像并转化为数字矩阵
print(img)
