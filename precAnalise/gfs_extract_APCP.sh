#! /bin/bash

echo "Limpando diretórios"
rm /dados/dmdpesq/Proj_GFS/etapa1/12/*
rm /dados/dmdpesq/Proj_GFS/etapa2/12/*
rm /dados/dmdpesq/Proj_GFS/etapa3/12/24/*
rm /dados/dmdpesq/Proj_GFS/etapa4/12/24/*
echo "Fim da limpeza"

inctime=/dados/dmdpesq/Proj_GFS/bin/inctime/inctime

gribs=/dados/dmdpesq/Proj_GFS/GFS 

#inctime
fct=24
#previ file gfs
#tfct=24
tfct=24 
i=12 
	
datai=20131231${i}
dataf=2014013118
data=${datai}
while [ ${data} -le ${dataf} ]
do
	yyyymm=$(echo ${data} | cut -c 1-6)
	ddhh=$(echo ${data} | cut -c 7-10)
	hh=$(echo ${data} | cut -c 9-10)
	dataanl=${data}
	echo "${hh}"
	echo "${yyyymm}/${ddhh}"
    fileout_acumula=etapa1/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.grib2
	for temp in $(seq -w 6 6 24)
	do
		echo "${temp}"
		#fileout_acumula=etapa1/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.grib2
		arq_prev=${gribs}/${yyyymm}/${ddhh}/gfs.t${hh}z.pgrb2f${temp}.${dataanl}.grib2
        #Extrai a variavel
		~/bin/wgrib2 $arq_prev -append -match "(:APCP:)" -grib  $fileout_acumula
	done

	fileout_nc=etapa2/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.nc #:TMP:surface:
    
    #Converte arquivo grib2 para netcdf
	~/bin/wgrib2 $fileout_acumula -netcdf ${fileout_nc}
     
	dataprev=$(${inctime} ${dataanl} +${fct}hr %y4%m2%d2%h2)
    
    #Calcular a somar dos passos de tempo
	cdo timselsum,8,0 ${fileout_nc} etapa3/${i}/${tfct}/gfs.t${hh}z.pgrb2f${tfct}.${dataprev}_APCP.nc	    

	data=$(${inctime} ${data} +${fct}hr %y4%m2%d2%h2)
done

#Juntar várias arquivos com váriáveis diferente em um único arquivo
cdo -r mergetime etapa3/12/24/*.nc etapa4/12/24/prev.2014.jan_APCP_12z_24h.nc

fileMergeInterp=/stornext/online8/bamc/w.santos/Experimento_umidade_do_solo/GFS/prec_201401.nc
fileGFS=/dados/dmdpesq/Proj_GFS/etapa4/12/24/prev.2014.jan_APCP_12z_24h.nc
fileOutGFSInterpMERGE=/dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan_APCP_12z_24h_interp.nc

#Interpolar uma grade Gaussiana qualquer (e.g. 384x190-cfs) para (128x64-echam)
cdo -r remapbil,${fileMergeInterp} ${fileGFS} ${fileOutGFSInterpMERGE}


exit 0
