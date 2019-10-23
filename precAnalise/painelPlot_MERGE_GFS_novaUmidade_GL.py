from PIL import Image 
import cv2
import numpy as np
from sys import exit

imgUmidade_GL = cv2.resize(
                    (cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_umidade_GL_PREC.png")
                    [1:3127, 799:2940]),
                    None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
imgNova_Umidade_do_Solo = cv2.resize(
                    (cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_Nova_Umidade_do_Solo_PREC.png")
                    [1:3127, 799:2940]),
                    None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
imgGFS = cv2.resize(
                    (cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/GFS_48h_12Z_.png")
                    [1:3127, 659:2940]),
                    None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
imgUMERGE = cv2.resize(
                    (cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/MERGE_JAN_12Z_.png")
                    [1:3127, 659:2940]),
                    None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)

legenda = cv2.resize(
                    (cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/legenda.jpg")
                    [1:3127, 1:1940]),
                    None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)

height, width, channels = imgUMERGE.shape
print(height, width, channels)
#height, width, channels = legenda.shape
#print(height, width, channels)

#legenda = cv2.resize(
#                    (cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_umidade_GL_PREC.png")
#                    [1:3127, 100:2940]),
#                    None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)

#Fileshape = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/legenda.jpg")
#
#height, width, channels = Fileshape.shape
#print(height, width, channels)
#
#exit(0)

im_v = cv2.hconcat([imgUMERGE,imgGFS,imgUmidade_GL,imgNova_Umidade_do_Solo])
#im_v2 = cv2.hconcat([legenda])
#
#im_v = cv2.hconcat([im_v1,im_v2])

cv2.imwrite('teste_campoEspacial.jpg', im_v)


###FIMMM


exit(0)







imgNova_Umidade_do_Solo = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/JAN2014_48h_12Z_Nova_Umidade_do_Solo_PREC.png")

imgGFS = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/GFS_24h_12Z_.png")

imgUMERGE = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/MERGE_JAN_12Z_.png")

###PREC 	
print(imgPREC.shape)
imgPREC_cropped = imgPREC[350:3127, 1:7540]
imgPREC_cropped_half = cv2.resize(imgPREC_cropped, (3580, 1500), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)


#exit(0)
###CLSF 	
print(imgCLSF.shape)
imgCLSF_cropped = imgCLSF[350:3127, 1:7540]
imgCLSF_cropped_half = cv2.resize(imgCLSF_cropped, (3580, 1500), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
height, width, channels = imgCLSF.shape
print (height, width, channels)
height, width, channels = imgCLSF_cropped_half.shape
print (height, width, channels)
###CSSF	
print(imgCSSF.shape)
imgCSSF_cropped = imgCSSF[350:3127, 1:7540]
imgCSSF_cropped_half = cv2.resize(imgCSSF_cropped, (3580, 1500), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
height, width, channels = imgCSSF.shape
print (height, width, channels)
height, width, channels = imgCSSF_cropped_half.shape
print (height, width, channels)
###CSSF	
print(imgUSSL.shape)
imgUSSL_cropped = imgUSSL[350:3127, 1:7540]
imgUSSL_cropped_half = cv2.resize(imgUSSL_cropped, (3580, 1500), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
height, width, channels = imgUSSL.shape
print (height, width, channels)
height, width, channels = imgUSSL_cropped_half.shape
print (height, width, channels)

#im_v = cv2.vconcat([cropped])
im_v1 = cv2.vconcat([imgPREC_cropped_half,imgCLSF_cropped_half,imgCSSF_cropped_half,imgUSSL_cropped_half])
im_v2 = cv2.vconcat([imgPREC_cropped_half,imgCLSF_cropped_half,imgCSSF_cropped_half,imgUSSL_cropped_half])
im_v = cv2.hconcat([im_v1,im_v2])
##Acrescentar titulo
##font = cv2.FONT_HERSHEY_DUPLEX
##cv2.putText(im_v,'Serie Temporal',(30,50), font, 2,(0,0,0), 3, 0)
cv2.imwrite('teste.jpg', im_v)