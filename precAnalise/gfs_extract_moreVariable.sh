#! /bin/bash

#https://www.nco.ncep.noaa.gov/pmb/products/gfs/gfs.t00z.pgrb2.0p25.f006.shtml

inctime=/dados/dmdpesq/Proj_GFS/bin/inctime/inctime

limpe_dir() {
    #funcao para limpar os dados anteriores
    echo "Limpando diretórios"
    rm /dados/dmdpesq/Proj_GFS/etapa1/12/*
    rm /dados/dmdpesq/Proj_GFS/etapa2/12/*
    rm /dados/dmdpesq/Proj_GFS/etapa3/12/${2}/*
    rm /dados/dmdpesq/Proj_GFS/etapa4/12/${2}/*
    rm /dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan_${1}_12z_${2}h_interp.nc
    echo "Fim da limpeza"

}

interp() {
    ##funcao para interpolar os dados
    dir_MergeInterp=/stornext/online8/bamc/w.santos/Experimento_umidade_do_solo/GFS
    dir_fileGFS=/dados/dmdpesq/Proj_GFS/etapa4/12/${2}
    dir_fileOutGFSInterpMERGE=/dados/dmdpesq/Experimento_umidade_do_solo/GFS

    fileMergeInterp=${dir_MergeInterp}/prec_201401.nc

    fileGFS=${dir_fileGFS}/prev.2014.jan_${1}_12z_${2}h.nc

    fileOutGFSInterpMERGE=${dir_fileOutGFSInterpMERGE}/prev.2014.jan_${1}_12z_${2}h_interp.nc

    fileconcatVars=${dir_fileOutGFSInterpMERGE}/prev.2014.jan_*_12z_${2}h_interp.nc

    fileconcatVars_out=${dir_fileOutGFSInterpMERGE}/prev.2014.jan_12z_${2}h_interp.nc


    #Interpolar uma grade Gaussiana qualquer (e.g. 384x190-cfs) para (128x64-echam)
    cdo -r remapbil,${fileMergeInterp} ${fileGFS} ${fileOutGFSInterpMERGE}
    #concatenar
    #cdo -r merge ${fileconcatVars} ${fileconcatVars_out}
        
}

var_0_6() {

    limpe_dir ${1} ${2} 

    gribs=GFS
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

        interp ${1} ${tfct}
}


var_6() {
    
    limpe_dir ${1} ${2} 

    gribs=GFS
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

        dataprev=$(${inctime} ${dataanl} +${tfct}hr %y4%m2%d2%h2)
    	fileout_nc=etapa3/${hh}/${tfct}/gfs.t${hh}z.pgrb2f${tfct}.${dataprev}_${1}.nc
        	
        arq_prev=${gribs}/${yyyymm}/${ddhh}/gfs.t${hh}z.pgrb2f${tfct}.${dataanl}.grib2
            
        #Extrai a variavel e converte arquivo grib2 para netcdf
        ~/bin/wgrib2 $arq_prev -match "(:${var}:2 m above ground)" -netcdf $fileout_nc  

       	data=$(${inctime} ${data} +${fct}hr %y4%m2%d2%h2)
    done
    #Juntar várias arquivos com váriáveis diferente em um único arquivo
    cdo -r mergetime etapa3/12/${tfct}/*201401*.nc etapa4/12/${tfct}/prev.2014.jan_${1}_12z_${tfct}h.nc

    interp ${1} ${tfct}
}


for var in "SPFH"  "TMP"
do
 
    for previsao in $(seq 24 24 168)
    do 
        echo "${var}" 
        echo "$previsao"

        var_6 ${var} ${previsao}
    done
done


prev_in=06
incr=24
for var in  "LHTFL" "APCP" "SHTFL"
do
    for previsao in $(seq 24 24 168) 
    do 
        
        echo "${var}"
        echo "$prev_in"
        echo "$previsao"
        
        var_0_6 ${var} ${previsao} ${prev_in}

        let prev_in=$(($prev_in+$incr))
        if [ $prev_in == 174 ] 
        then
            echo "ok"
            prev_in=06
        fi

    done
done

