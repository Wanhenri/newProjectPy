from PIL import Image 
import cv2
import numpy as np
from sys import exit

Fileshape = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_umidade_GL_PREC.png")

legenda = cv2.resize(
                    (cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_umidade_GL_PREC.png")
                    [3162:3562, 1:3607]),
                    None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)

height, width, channels = Fileshape.shape
print(height, width, channels)

legenda = cv2.rotate(legenda, cv2.ROTATE_90_COUNTERCLOCKWISE)

im_v = cv2.hconcat([legenda])


cv2.imwrite('legenda.jpg', im_v)