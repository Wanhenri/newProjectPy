#! /bin/bash


cria_ctl() {
cat << EOF > ${3}
dset ^GL_SM.GPNR.${1}.gra
options sequential
undef -1
title SOIL MOISTURE output
xdef 1440 linear        -179.875          0.250
ydef  720 linear         -89.875          0.250
zdef 8 levels -3.25  -2.125 -1.375  -0.75 -0.375 -0.19 -0.09 -0.025
tdef    1 linear ${2}  1dy
vars    2
us         8   99 umid do solo  [mm^3/mm^3]
rr         0   99 precipitacao  [mm]
endvars
EOF
}


#datai=2013120100
#dataf=2013123100

datai=2013120100
dataf=2014013100

data=${datai}

while [ ${data} -le ${dataf} ]
do

  echo ${data:8:10}
 
  datafmt=$(${inctime} ${data} +0d %h2Z%d2%MC%y4)
  
  echo "data format ${datafmt}"
  echo "data ${data}"

  arqctl="./dados/GL_SM.GPNR.${data}.ctl"
  arqnc="./dados/GL_SM.GPNR.${data}.nc"

  cria_ctl ${data} ${datafmt} ${arqctl}
 
  cdo -f nc import_binary dados/GL_SM.GPNR.${data}.ctl dados/GL_SM.GPNR.${data}.nc
  data=$(${inctime} ${data} +12hr %y4%m2%d2%h2)

  

done

exit 0

