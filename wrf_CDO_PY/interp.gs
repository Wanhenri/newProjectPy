#! /bin/bash

inctime=/stornext/home/carlos.bastarz/bin/inctime

datai=20180801
dataf=20180930
#dataf=20180802


#wrfout_d01_2018-08-24_23:00:00

data=${datai}

while [ ${data} -le ${dataf} ]
do
        dataday=` echo ${data} |cut -c7-8`
        datamonth=` echo ${data} |cut -c5-6`
        echo "${dataday}"

        #RAINC RAINNC co o3 TAUAER3 PM2_5_DRY V10 U10
        for var in RAINNC;
        do
                for i in $(seq -w 0 23)
                do
                        cdo remapbil,prec_201808.nc new_files/wrfout_d01_2018-${datamonth}-${dataday}_${i}:00:00_${var}.nc interp/wrfout_d01_2018-${datamonth}-${dataday}_${i}:00:00_${var}_interp.nc
                done
                data=$(${inctime} ${data} +1d %y4%m2%d2)
        done
done
exit 0
