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
#echo "${dataday}"

	for i in $(seq -w 0 3 23)
        do
	
	echo "${i}"	
#echo "cdo -f nc import_binary profile_2018093000G-A-2018-09-30-${i}0000-g1.ctl profile_2018093000G-A-2018-09-30-${i}0000-g1.nc"
	echo "cdo -f nc import_binary profile_${data}00G-A-2018-${datamonth}-${dataday}-${i}0000-g1.ctl profile_${data}00G-A-2018-${datamonth}-${dataday}-${i}0000-g1.nc"
	cdo -f nc import_binary profile_${data}00G-A-2018-${datamonth}-${dataday}-${i}0000-g1.ctl profile_${data}00G-A-2018-${datamonth}-${dataday}-${i}0000-g1.nc	

	done
	data=$(${inctime} ${data} +1d %y4%m2%d2)
done
exit 0

