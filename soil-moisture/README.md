# Manual para realização de experimentos com umidade do solo

### Dados Salvos no tupã:
- /stornext/online8/bamc/w.santos/Experimento_umidade_do_solo/Experimento_com_GL_SM

## Baixando modelo
Para baixar a versão do modelo BAM utilizado nos experimentos, foi utilizado essa wiki:

- https://projetos.cptec.inpe.br/projects/smg/wiki/V210_LukeSkywalker

## Namelist do runPre
**caminho:**  /scratchin/grupos/bamc/home/w.santos/SMG/run/scripts/bam_scripts

- namelist.runPre

**Parametros:**
- SoilMoistureWeeklyCPTEC = 1
- SoilMoistureWeekly      = 1

## Dados de umidade do solo utilizado na operação
Ex.:

- /home/smagnum/Documentos/umidade_do_solo

GL_SM.GPNR.2014011412.vfm.gz

GL_SM.GPNR.2014011412.vfm

## script para baixar dados de umidade do solo do site do Brams
```shell
#! /bin/bash

#  Categories:
#    Baixar Umidade do Solo
#
#  Author:
#    Carlos Frederico Bastarz
#    Wanderson Henrique dos Santos

#inctime=/usr/local/bin/inctime

#datai=2013120100
#dataf=2013123100

datai=2013122100
dataf=2014020100

data=${datai}

while [ ${data} -le ${dataf} ]
do

  echo ${data}

  wget -c http://ftp1.cptec.inpe.br/brams/data-brams/soil-moisture/${data:0:4}/GPNR/GL_SM.GPNR.${data}.vfm.gz
  wget -c http://ftp1.cptec.inpe.br/brams/data-brams/soil-moisture/${data:0:4}/GPNR/GL_SM.GPNR.${data}.gra.gz
  wget -c http://ftp1.cptec.inpe.br/brams/data-brams/soil-moisture/${data:0:4}/GPNR/GL_SM.GPNR.${data}.ctl.gz

  gzip -d GL_SM.GPNR.${data}.vfm.gz
  gzip -d GL_SM.GPNR.${data}.gra.gz
  gzip -d GL_SM.GPNR.${data}.ctl.gz

  cdo -f nc import_binary GL_SM.GPNR.${data}.ctl GL_SM.GPNR.${data}.nc

 
  data=$(${inctime} ${data} +12hr %y4%m2%d2%h2)

done

cdo -r mergetime GL_SM.GPNR.201401**12.nc GL_SM.GPNR.20140112.nc

exit 0


```

## Dados do Luis Gonçalves

**caminho:** /scratchin/grupos/wrf/home/luis.goncalves/valida/BAM/mcga

Arquivo fornecido:
- /scratchout/grupos/apgmet/home/vivian.bauce/bam_ldas/12Z

https://www.itjobs.pt/emprego/python

(???)
Idim=1440
Jdim=720
Kdim=8

Renomear para SoilMoistureWeekly.*anomesdia*

**caminho:**  /scratchin/grupos/bamc/home/w.santos/SMG/run/scripts/bam_scripts

- namelist.runPre

**Parametros:**
- SoilMoistureWeeklyCPTEC = 0
- SoilMoistureWeekly  = 1

### Rodando o pré-processamento
***
Para Rodar o pré-processamento vamos precisar dos scripts:
- get_icn.bash
- roda_modificado_v1.sh
- namelist.runPre
- runPre
- + *./runPre ${TRUNC} ${LEV}  ${DATA} NMC 1 T F 574 64*

### Rodando o modelo
***
Para Rodar o modelo vamos precisar dos scripts:
- get_icn.bash
- roda_modificado_v1.sh
- runModel
- + *./runModel -np 480 -N 4 -d 6 -t 299 -l 64 -I ${LABELI} -F ${LABELF} -ts 6 -i 2 -p SMT -s sstwkl*

### Rodando o pré-processamento
***
Para Rodar o pré-processamento vamos precisar dos scripts:
- get_icn.bash
- roda_modificado_v1.sh
- runPos


</br >
</br >
</br >
</br >
<h1>Anexos</h1>


#### Os scripts utilizado
***

### get_icn.bash
```shell
#!/bin/bash 
#help#
#*********************************************************************************************************#
#                                                                                                         #
# script to run CPTEC Global Model on PC Clusters under MPI Scali                                         #
# and Sun Grid Engine without OpenMP                                                                      #
#                                                                                                         #
# assumptions: assume present at the same directory:                                                      #
#              ParModel_MPI (Global Model Executable file)                                                #
#              MODELIN (Global Model input Namelist file)                                                 #
#                                                                                                         #
# usage: ./get_icn.bash TRUNC LEV LABELI NFDAYS                                                           #
# where:                                                                                                  #
# LABELI:: initial condition data                                                                         #
# cpu_mpi: integer, the desired number of mpi processes                                                   #
# cpu_node: integer, the desired number of mpi processes per shared memory node                           #
# name: character, the job name (for SGE)                                                                 #
# initlz  =2,     ! initlz =2 diabatic initialization and normal mode initialization                      #
#                 !        =1 diabatic initialization and without normal mode initialization              #
#                 !        =0 without diabatic initialization and without normal mode initialization      #
#                 !           [TOTAL RESTART ](adiabatic with no normal mode initialization)              #
#                 !        <0 same as >0 with sib variables read in instead of  initialized               #
#                 !        =-1 diabatic initialization and without normal mode initialization             #
##!/bin/bash 
#help#
#*********************************************************************************************************#
#                                                                                                         #
# script to run CPTEC Global Model on PC Clusters under MPI Scali                                         #
# and Sun Grid Engine without OpenMP                                                                      #
#                                                                                                         #
# assumptions: assume present at the same directory:                                                      #
#              ParModel_MPI (Global Model Executable file)                                                #
#              MODELIN (Global Model input Namelist file)                                                 #
#                                                                                                         #
# usage: ./get_icn.bash TRUNC LEV LABELI NFDAYS                                                           #
# where:                                                                                                  #
# LABELI:: initial condition data                                                                         #
# cpu_mpi: integer, the desired number of mpi processes                                                   #
# cpu_node: integer, the desired number of mpi processes per shared memory node                           #
# name: character, the job name (for SGE)                                                                 #
# initlz  =2,     ! initlz =2 diabatic initialization and normal mode initialization                      #
#                 !        =1 diabatic initialization and without normal mode initialization              #
#                 !        =0 without diabatic initialization and without normal mode initialization      #
#                 !           [TOTAL RESTART ](adiabatic with no normal mode initialization)              #
#                 !        <0 same as >0 with sib variables read in instead of  initialized               #
#                 !        =-1 diabatic initialization and without normal mode initialization             #
#                 !            with sib variables read in instead of  initialized                         #
#                 !        =-2 diabatic initialization and normal mode initialization                     #
#                 !            with sib variables read in instead of  initialized                         #
# hold: any, present or not;                                                                              #
#            if absent, script finishes after queueing job;                                               #
#            if present, script holds till job completion                                                 #
#*********************************************************************************************************#
#help#
#
#       Help:
#
if [ "${1}" = "help" -o -z "${1}" ]
then
                 !            with sib variables read in instead of  initialized                         #
#                 !        =-2 diabatic initialization and normal mode initialization                     #
#                 !            with sib variables read in instead of  initialized                         #
# hold: any, present or not;                                                                              #
#            if absent, script finishes after queueing job;                                               #
#            if present, script holds till job completion                                                 #
#*********************************************************************************************************#
#help#
#
#       Help:
#
if [ "${1}" = "help" -o -z "${1}" ]
then
  cat < ${0} | sed -n '/^#help#/,/^#help#/p'
  exit 1
else
  DATA=`echo ${1} | awk '{print $1/1}'`
fi
TRUNC=${1}
LEV=${2}
DATA=${3}
NFDAYS=${4}
DATADIR=`echo ${DATA} |cut -c1-8`
HH=`echo ${DATA} |cut -c9-10`
DATADIR1=`echo ${DATA} |cut -c1-6`
HH1=`echo ${DATA} |cut -c7-10`

LABELI=${DATA}
calday ()
{
yi=`echo ${LABELI} |awk '{ print( substr($1,1,4)/1) }'`
mi=`echo ${LABELI} |awk '{ print( substr($1,5,2)/1) }'`
di=`echo ${LABELI} |awk '{ print( substr($1,7,2)/1) }'`
hi=`echo ${LABELI} |awk '{ print( substr($1,9,2)/1) }'`

let ybi=${yi}%4
if [ ${ybi} = 0 ];then
    declare -a md=( 31 29 31 30 31 30 31 31 30 31 30 31 )
else
    declare -a md=( 31 28 31 30 31 30 31 31 30 31 30 31 )
fi
let df=${di}+${NFDAYS}
let mf=${mi}
let yf=${yi}
let hf=${hi}
let n=${mi}-1
if [ ${df} -gt ${md[${n}]} ]
then
let df=${df}-${md[${n}]}
let mf=${mf}+1
if [ ${mf} -eq 13 ]
then
let mf=1
let yf=${yf}+1
fi
fi
if [ ${df} -lt 10 ]
then DF=0${df}
else DF=${df}
fi
if [ ${mf} -lt 10 ]
then MF=0${mf}
else MF=${mf}
fi
YF=${yf}
if [ ${hf} -lt 10 ]
then HF=0${hf}
else HF=${hf}
fi
}

calday
LABELF=${YF}${MF}${DF}${HF}
echo $LABELF
#As duas linhas abaixo sao para rodar o runPre, que sera acionado pelo script roda
#./runPre ${TRUNC} ${LEV}  ${DATA} NMC 0 T
###./runPre ${TRUNC} ${LEV}  ${DATA} NMC 1 T F 574 64
###echo "runPre ${TRUNC} ${LEV} ${DATA} ${NFDAYS}  NMC 1 T F 574 64"


it=1
export FIRST='     '
export SECOND='     '
itr=0
nProc=`printf "WM%10.10d  \n" ${LABELI}`

export it
# Caso for rodar o runModel, desabilitar essa opcao
# As duas linhas abaixo
#./runModel 240 4 6  ${nProc} ${TRUNC} ${LEV} ${LABELI} ${LABELF} ${LABELF} NMC sstwkl 2

#> mudanca no SMT  ---> ./runModel -np 480 -N 4 -d 6 -t 299 -l 64 -I ${LABELI} -F ${LABELF} -ts 6 -i 2 -p SMT -s sstwkl
#./runModel -np 480 -N 4 -d 6 -t 299 -l 64 -I ${LABELI} -F ${LABELF} -ts 6 -i 2 -p CPT -s sstwkl
./runModel -np 480 -N 4 -d 6 -t 299 -l 64 -I ${LABELI} -F ${LABELF} -ts 6 -i 2 -p SMT -s sstwkl
echo "./runModel -np 480 -N 4 -d 6 -t 299 -l 64 -I ${LABELI} -F ${LABELF} -ts 6 -i 2 -p CPT -s sstwkl"
#echo "./runModel 240 4 6  ${nProc} ${TRUNC} ${LEV} ${LABELI} ${LABELF} ${LABELF} NMC sstwkl 2"
export FIRST=`qstat | grep -i ${nProc} | awk '{print $1}'`
let it=${it}+1

export it
nProc=`printf "WP%4.4d  \n" ${LABELI}`
#Caso for rodar o runPos, desabilitar essa opcao
#As duas linhas abaixo
#./runPos 360 1 ${nProc} ${TRUNC} ${LEV}  ${LABELI} ${LABELF}  NMC hold
#./runPos 120 24 1 ${nProc} ${TRUNC} ${LEV}  ${LABELI} ${LABELF}  NMC COLD
##./runPos -np 480 -N 4 -d 6 -t 299 -l 64 -I ${LABELI} -F ${LABELF}  -p CPT -ft p
##echo "./runPos -np 480 -N 4 -d 6 -t 299 -l 64 -I ${LABELI} -F ${LABELF}  -p CPT -ft p"
#echo "./runPos 120 24 1 ${nProc} ${TRUNC} ${LEV}  ${LABELI} ${LABELF}  NMC COLD"
let it=${it}+1

let itr=${itr}+1
exit
```

### roda_modificado_v1.sh
```shell
#!/bin/bash

echo "Digite o periodo inicial: yyyymmddhh"
read datainicial

#variavel finaliza a contagem infinita gerada
echo "Digite o periodo final: yyyymmddhh"
read final

echo "     "

#incremento
incr=`echo ${datainicial} |cut -c9-10`

while : ;do

    datafi=$($inctime ${datainicial} +${incr}h %y4%m2%d2%h2)
    let incr=$incr+12
    #let incr=$incr+06
    echo ${datafi}

    ./get_icn.bash 299 64 ${datafi} 8
    echo "299 64 ${datafi} 6"

    while [ `qstat | grep w.santos | wc -l` -ge 8 ];do
          sleep 10
    done

    #Assim que alcancar a data final desejada, ele realiza um break nesse looping infinito
    if [ ${datafi} -eq ${final} ]
    then
       break
    fi
done

```
