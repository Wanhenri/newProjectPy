#! /bin/bash

inctime=/dados/dmdpesq/Proj_GFS/bin/inctime/inctime

gribs=/dados/dmdpesq/Proj_GFS/GFS 

#inctime
fct=24
#previ file gfs
#tfct=24
for tfct in $(seq -w 24 24 48)
do
	#for i in $(seq -w 0 12 12)
	for i in $(seq -w 12 12 12)
	do
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
			for temp in $(seq -w 0 3 24)
			do
				echo "${temp}"
				fileout_acumula=etapa1/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.grib2
				arq_prev=${gribs}/${yyyymm}/${ddhh}/gfs.t${hh}z.pgrb2f${temp}.${dataanl}.grib2
				echo "acumula APCP ${arq_prev}"
				~/bin/wgrib2 $arq_prev -append -match "(:APCP:)" -grib  $fileout_acumula
			done
			fileout_nc=etapa2/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.nc #:TMP:surface:
			~/bin/wgrib2 $fileout_acumula -netcdf ${fileout_nc}
       
			dataprev=$(${inctime} ${dataanl} +${fct}hr %y4%m2%d2%h2)
			echo "data previsao ${dataprev}"
			cdo timselsum,8,0 ${fileout_nc} etapa3/${i}/${tfct}/gfs.t${hh}z.pgrb2f${tfct}.${dataprev}_APCP.nc	    
			echo "previsao: ${tfct}"
			echo "ARQUIVO DE ENTRADA  ${arq}"
			echo "ARQUIVO DE SAIDA ETAPA 1 ${fileout}"
			echo "ARQUIVO DE SAIDA ETAPA 2 ${fileout_nc}"
			data=$(${inctime} ${data} +${fct}hr %y4%m2%d2%h2)
		done
	done
done


#for tfct in $(seq -w 24 24 24)
#do
#    for i in $(seq -w 12 12 12)
#    do
#        echo "previsao: ${tfct}"
#        echo "${i}"
#        echo "cdo -r mergetime etapa3/${i}/${tfct}/gfs.t${i}z.pgrb2f${tfct}.201401??${i}_APCP.nc etapa4/${i}/${tfct}/prev.2014.jan_APCP_${i}z_${tfct}h.nc" 
#        cdo -r mergetime /dados/dmdpesq/Proj_GFS/etapa3/${i}/${tfct}/gfs.t${i}z.pgrb2f${tfct}.201401??${i}_APC.nc /dados/dmdpesq/Proj_GFS/etapa4/${i}/${tfct}/prev.2014.jan_APCP_${i}z_${tfct}h.nc
#        
#        fileMergeInterp=/stornext/online8/bamc/w.santos/Experimento_umidade_do_solo/GFS/prec_201401.nc
#
#        fileGFS=/dados/dmdpesq/Proj_GFS/etapa4/${i}/${tfct}/prev.2014.jan_APCP_${i}z_${tfct}h.nc
#
#        fileOutGFSInterpMERGE=/dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan_APCP_${i}z_${tfct}h_interp.nc
#        
#        cdo -r remapbil,${fileMergeInterp} ${fileGFS} ${fileOutGFSInterpMERGE}
#    done
#done
cdo -r mergetime etapa3/12/24/*.nc etapa4/12/24/prev.2014.jan_APCP_12z_24h.nc

fileMergeInterp=/stornext/online8/bamc/w.santos/Experimento_umidade_do_solo/GFS/prec_201401.nc
fileGFS=/dados/dmdpesq/Proj_GFS/etapa4/12/24/prev.2014.jan_APCP_12z_24h.nc
fileOutGFSInterpMERGE=/dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan_APCP_12_24h_interp.nc

cdo -r remapbil,${fileMergeInterp} ${fileGFS} ${fileOutGFSInterpMERGE}


exit 0

#cdo -r mergetime etapa3/12/24/gfs.tz.pgrb2f24.201401??12_APCP.nc etapa4/12/24/prev.2014.jan_APCP_12z_24h.nc
#cdo -r mergetime etapa3/${i}/${tfct}/gfs.t${hh}z.pgrb2f${tfct}.201401??${i}_APC.nc etapa4/${i}/${tfct}/prev.2014.jan_APCP_${i}z_${tfct}h.nc