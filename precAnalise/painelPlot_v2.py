###########3
#######ESSA É UMA VERSÃO QUE ESTA OK PARA DUAS COLUNAS DE FIGURAS EM GRAFICO DE SÉRIE TEMPORAL
from PIL import Image 
import cv2
import numpy as np
from sys import exit

#Relative Path 
#Image on which we want to paste 
imgPREC = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_PREC.png")
#imgPREC = cv2.resize(imgPREC, (3287,7685))
imgCLSF = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_CLSF.png")
#imgPREC = cv2.resize(imgCLSF, (125, 200))
imgCSSF = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_CSSF.png")
#imgCSSF = cv2.resize(imgCSSF, (125, 200))
imgUSSL = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_USSL.png")
imgUZRS = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_UZRS.png")
imgUZDS = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_UZDS.png")
imgT2MT = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_T2MT.png")
imgQ2MT = cv2.imread("/dados/dmdpesq/Experimento_umidade_do_solo/out/previsao_144_regiao_SUL_B1_SerieTemporal_Q2MT.png")  

###PREC 	
print(imgPREC.shape)
imgPREC_cropped = imgPREC[350:3127, 1:7540]
imgPREC_cropped_half = cv2.resize(imgPREC_cropped, (3580, 1500), fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
height, width, channels = imgPREC.shape
print (height, width, channels)
height, width, channels = imgPREC_cropped_half.shape
print (height, width, channels)
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