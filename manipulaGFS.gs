#! /bin/bash

inctime=/stornext/home/carlos.bastarz/bin/inctime

datai=20140101
dataf=20140131
#dataf=20180802


data=${datai}

vars=(TMP_surface)
# TMP_2maboveground
# TMP_surface
for var in "${vars[@]}";
do

	while [ ${data} -le ${dataf} ]
	do
		dataday=` echo ${data} |cut -c7-8`
		datamonth=` echo ${data} |cut -c5-6`
		echo "${dataday}"
	
		for i in $(seq  24 24 168);
		do
			echo "cdo select,name=${var} fcst.${data}12.${i}.nc out/fcst.${data}12.${i}_${var}.nc"
			cdo select,name=${var} fcst.${data}12.${i}.nc out/fcst.${data}12.${i}_${var}.nc
		done	
		data=$(${inctime} ${data} +1d %y4%m2%d2)
	done
#done

	echo "********"
	echo "Concatenar cada previsao"
	echo "********"

#for var in TMP_2maboveground;
#do
	for i in $(seq  24 24 168)
	do
		echo "cdo -r mergetime out/fcst.201401??12.${i}_${var}.nc out/prev.2014.jan.${i}_${var}.nc"
		cdo -r mergetime out/fcst.201401??12.${i}_${var}.nc out/prev.2014.jan.${i}_${var}.nc
	done
done

exit 0
