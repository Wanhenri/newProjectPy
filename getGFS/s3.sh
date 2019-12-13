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
        datai=20131225${i}
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

            arq=${gribs}/${yyyymm}/${ddhh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}.grib2
            fileout=etapa1/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.grib2

            fileout_nc=etapa2/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.nc #:TMP:surface:

            ~/bin/wgrib2 $arq -append -match "(:TMP:2 m above ground:)" -grib  $fileout
            for temp in $(seq -w 0 3 24)
            do
		        echo "${temp}"
		        fileout_acumula=etapa1/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_APCP.grib2
		        arq_prev=${gribs}/${yyyymm}/${ddhh}/gfs.t${hh}z.pgrb2f${temp}.${dataanl}.grib2
                	echo "acumula APCP ${arq_prev}"
                	~/bin/wgrib2 $arq_prev -append -match ":APCP:" -grib  $fileout_acumula
            done

	    ~/bin/wgrib2 $fileout_acumula -netcdf ${fileout_nc}
	    #~/bin/wgrib2 $fileout -netcdf ${fileout_nc}
            
	    dataprev=$(${inctime} ${dataanl} +${fct}hr %y4%m2%d2%h2)
	    echo "data previsao ${dataprev}"
	    cdo timselsum,8,0 ${fileout_nc} etapa3/${i}/gfs.t${hh}z.pgrb2f${tfct}.${dataprev}_APCP.nc	    
 
            echo "previsao: ${tfct}"
            #echo "ARQUIVO DE ENTRADA  ${arq}"
            #echo "ARQUIVO DE SAIDA ETAPA 1 ${fileout}"
            #echo "ARQUIVO DE SAIDA ETAPA 2 ${fileout_nc}"

            data=$(${inctime} ${data} +${fct}hr %y4%m2%d2%h2)
        done
    done
done

for tfct in $(seq -w 24 24 24)
do
    for i in $(seq -w 12 12 12)
    do

	echo "previsao: ${tfct}"
        echo "${i}"
	echo "cdo -r mergetime etapa3/${i}/gfs.tz.pgrb2f${tfct}.201401??${i}_APCP.nc etapa4/${i}/prev.2014.jan_APCP_${i}z_${tfct}h.nc"
        cdo -r mergetime etapa3/${i}/gfs.t${hh}z.pgrb2f${tfct}.${dataprev}_APCP.nc etapa4/${i}/prev.2014.jan_APCP_${i}z_${tfct}h.nc
    done
done

exit 0
