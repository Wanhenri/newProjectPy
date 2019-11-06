####################Etapa exclusiva para duas variaveis
ESTE REALIZADO COM SUCESSO
var_Heat_Net_Flux() {
    
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
        ~/bin/wgrib2 $arq_prev -match "(:${var}:)" -netcdf $fileout_nc  

       	data=$(${inctime} ${data} +${fct}hr %y4%m2%d2%h2)
    done
    #Juntar várias arquivos com váriáveis diferente em um único arquivo
    cdo -r mergetime etapa3/12/${tfct}/*201401*.nc etapa4/12/${tfct}/prev.2014.jan_${1}_12z_${tfct}h.nc

    interp ${1} ${tfct}
}

var=SHTFL
previsao=24
var_Heat_Net_Flux ${var} ${previsao}

#####################################################
