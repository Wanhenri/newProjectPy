#! /bin/bash

#inctime=/usr/local/bin/inctime

#datai=2013120100
#dataf=2013123100

datai=2013120100
dataf=2014013100

data=${datai}

while [ ${data} -le ${dataf} ]
do

  echo ${data}

  wget -c http://ftp1.cptec.inpe.br/brams/data-brams/soil-moisture/${data:0:4}/GPNR/GL_SM.GPNR.${data}.gra.gz


  gzip -d GL_SM.GPNR.${data}.gra.gz

 
  data=$(${inctime} ${data} +12hr %y4%m2%d2%h2)

done

exit 0

