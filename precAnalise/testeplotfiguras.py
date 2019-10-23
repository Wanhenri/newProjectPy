from __future__ import print_function
import os

from PIL import Image
import cv2
import numpy as np

#files = [
#  '/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_umidade_GL_PREC.png',
#  '/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_Nova_Umidade_do_Solo_PREC.png',
#  '/dados/dmdpesq/Experimento_umidade_do_solo/out/GFS_48h_12Z_.png',
#  '/dados/dmdpesq/Experimento_umidade_do_solo/out/MERGE_JAN_12Z_.png',
#  '/dados/dmdpesq/Experimento_umidade_do_solo/legenda.jpg']

imgUmidade_GL = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_umidade_GL_PREC.png")[1:3127, 799:2940]
                    
imgNova_Umidade_do_Solo = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_Nova_Umidade_do_Solo_PREC.png")[1:3127, 799:2940]
                    
imgGFS = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/GFS_48h_12Z_.png")[1:3127, 659:2940]
                    
imgUMERGE = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/MERGE_JAN_12Z_.png")[1:3127, 659:2940]
                    

files = [imgUmidade_GL,imgNova_Umidade_do_Solo,imgGFS,imgUMERGE]


result = Image.new("RGB", (850, 850))

for index, file in enumerate(files):
  path = os.path.expanduser(file)
  img = Image.open(path)
  img.thumbnail((400, 400), Image.ANTIALIAS)
  x = index // 2 * 400
  y = index % 2 * 400
  w, h = img.size
  print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
  result.paste(img, (x, y, x + w, y + h))

result.save(os.path.expanduser('image.jpg'))