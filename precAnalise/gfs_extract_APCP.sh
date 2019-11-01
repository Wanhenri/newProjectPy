#! /bin/bash

inctime=/dados/dmdpesq/Proj_GFS/bin/inctime/inctime

var_0_6() {

    echo "Limpando diretórios"
    rm /dados/dmdpesq/Proj_GFS/etapa1/12/*
    rm /dados/dmdpesq/Proj_GFS/etapa2/12/*
    rm /dados/dmdpesq/Proj_GFS/etapa3/12/${2}/*
    rm /dados/dmdpesq/Proj_GFS/etapa4/12/${2}/*
    rm /dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan_${1}_12z_${2}h_interp.nc
    echo "Fim da limpeza"

    gribs=/dados/dmdpesq/Proj_GFS/GFS
    #pre inctime
    fct=24
    #previ file gfs
    tfct=${2} 
    i=12 
    
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
            fileout_acumula=etapa1/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_${1}.grib2
        	for temp in $(seq -w ${3} 6 ${2})
        	do
        		echo "${temp}"
        		arq_prev=${gribs}/${yyyymm}/${ddhh}/gfs.t${hh}z.pgrb2f${temp}.${dataanl}.grib2
                #Extrai a variavel
        		~/bin/wgrib2 $arq_prev -append -match "(:${1}:)" -grib  $fileout_acumula
        	done

        	fileout_nc=etapa2/${hh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}_${1}.nc #:TMP:surface:

            #Converte arquivo grib2 para netcdf
        	~/bin/wgrib2 $fileout_acumula -netcdf ${fileout_nc}

        	#dataprev=$(${inctime} ${dataanl} +${fct}hr %y4%m2%d2%h2)
            dataprev=$(${inctime} ${dataanl} +${tfct}hr %y4%m2%d2%h2)

            #Calcular a somar dos passos de tempo
        	cdo timselsum,28,0 ${fileout_nc} etapa3/${i}/${tfct}/gfs.t${hh}z.pgrb2f${tfct}.${dataprev}_${1}.nc	    

        	data=$(${inctime} ${data} +${fct}hr %y4%m2%d2%h2)
        done
        #Juntar várias arquivos com váriáveis diferente em um único arquivo
        cdo -r mergetime etapa3/12/${tfct}/*201401*.nc etapa4/12/${tfct}/prev.2014.jan_${1}_12z_${tfct}h.nc

        fileMergeInterp=/stornext/online8/bamc/w.santos/Experimento_umidade_do_solo/GFS/prec_201401.nc
        fileGFS=/dados/dmdpesq/Proj_GFS/etapa4/12/${tfct}/prev.2014.jan_${1}_12z_${tfct}h.nc
        fileOutGFSInterpMERGE=/dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan_${1}_12z_${tfct}h_interp.nc
        #Interpolar uma grade Gaussiana qualquer (e.g. 384x190-cfs) para (128x64-echam)
        cdo -r remapbil,${fileMergeInterp} ${fileGFS} ${fileOutGFSInterpMERGE}
}

var=APCP
previsao=24
prev_in=06
while [[  $previsao -lt 192 ]] || [[  $prev_in -lt 174 ]]; do
    echo "$previsao"
    echo "$prev_in"
    
    var_0_6 ${var} ${previsao} ${prev_in}
    
    let previsao=previsao+24; 
    let prev_in=prev_in+24; 
done





#var=APCP
#previsao=96
#prev_in=78
#
#var_0_6 ${var} ${previsao} ${prev_in}
#####
#Como funciona?
#var=APCP
#previsao=(24 48 72 96 120 144 168)
#prev_in=(06 30 54 78 102 126 150)
#
#CONTADOR=0
#while [  $CONTADOR -lt 7 ]; do
#    echo "$CONTADOR"
#    for ((i=0; i<${#previsao[@]}; i++)); do
#        echo "variavel: ${var}  | previsao: ${previsao[i]} |  prev_in:  ${prev_in[i]}  " 
#        var_0_6 ${var} ${previsao[i]} ${prev_in[i]}
#        #var_0_6 ${var} ${previsao} ${prev_in}
#    done
#    let CONTADOR=CONTADOR+1; 
#done

#Exemplo
#ARR_MPOINT=(24 48 72 96 120 144 168)
#ARR_LVNAME=(06 30 54 78 102 126 150)
#
#for ((i=0; i<${#ARR_MPOINT[@]}; i++)); do
#    echo "${ARR_LVNAME[i]}     ${ARR_MPOINT[i]}  " 
#done
