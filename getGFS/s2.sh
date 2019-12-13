for arq in $(ls GFS/201401/0112/*grib2)
do

  anl=$(basename $arq | awk -F "." '{print $4}')
  hr=$(basename $arq | awk -F "." '{print $3}' | cut -c 7-10)
  fct=$(/stornext/home/carlos.bastarz/bin/inctime $anl +${hr}hr %y4%m2%d2%h2)

  echo "arquivo: $arq - horas de previsao $hr - (analise $anl - arquivo de previsao $fct)"

done
 