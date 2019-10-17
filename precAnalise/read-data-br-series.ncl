load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begin


;>>>>>>>BAM com dados de assimilacao<<<<<<<<<
new1 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/JAN2014_24Z_12Z_interp.nc", "r")
new1_24=new1->prec
new1_24@_FillValue=-9.99e+08; -9999

new1 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/JAN2014_48Z_12Z_interp.nc", "r")
new1_48=new1->prec
new1_48@_FillValue=-9.99e+08; -9999

new1 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/JAN2014_72Z_12Z_interp.nc", "r")
new1_72=new1->prec
new1_72@_FillValue=-9.99e+08; -9999
;*
;*
;*
;>>>>>>>BAM dados NCEP<<<<<<<<<<<<<<<<<<<<<<
fall2 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/JAN2014_24Z_12Z_interp.nc", "r")
new2_24 = fall2->prec
new2_24@_FillValue=-9.99e+08; -9999

fall2 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/JAN2014_48Z_12Z_interp.nc", "r")
new2_48 = fall2->prec
new2_48@_FillValue=-9.99e+08; -9999

fall2 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/JAN2014_72Z_12Z_interp.nc", "r")
new2_72 = fall2->prec
new2_72@_FillValue=-9.99e+08; -9999
;*
;*
;*
;>>>>>>>GFS<<<<<<<<<<<<<<<<<<<<<<
fall3 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan.24h_interp.nc", "r")
gfs_24 = fall3->APCP_surface
gfs_24@_FillValue=-9.99e+08

fall3 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan.48h_interp.nc", "r")
gfs_48 = fall3->APCP_surface
gfs_48@_FillValue=-9.99e+08

fall3 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/GFS/prev.2014.jan.72h_interp.nc", "r")
gfs_72 = fall3->APCP_surface
gfs_72@_FillValue=-9.99e+08
;*
;*
;*
;>>>>>IMERG
fall3 = addfile ("/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/prec_201401.nc","r")
tmpa = fall3->prec

;>>>>>>>>>>>>>>America do Sul
;media do observado
;=wgt_areaave(tmpa(:,:,:),1.0,1.0,1)
aa1o=dim_avg_Wrap(dim_avg_Wrap(tmpa(:,{-36:0},{280:325})))
print(aa1o)
write_table("teste.txt","w",[/aa1o/],"%2.6f")
;---- 24hrs
n1m24=dim_avg_Wrap(dim_avg_Wrap(new1_24(:,{-36:0},{280:325})))
aa1m24=dim_avg_Wrap(dim_avg_Wrap(new2_24(:,{-36:0},{280:325})))       
gfs1m24=dim_avg_Wrap(dim_avg_Wrap(gfs_24(:,{-36:0},{280:325})))       

;---- 48hrs
n1m48=dim_avg_Wrap(dim_avg_Wrap(new1_48(:,{-36:0},{280:325})))
aa1m48=dim_avg_Wrap(dim_avg_Wrap(new2_48(:,{-36:0},{280:325}))) 
gfs1m48=dim_avg_Wrap(dim_avg_Wrap(gfs_48(:,{-36:0},{280:325}))) 

;---- 72hrs
n1m72=dim_avg_Wrap(dim_avg_Wrap(new1_72(:,{-36:0},{280:325})))
aa1m72=dim_avg_Wrap(dim_avg_Wrap(new2_72(:,{-36:0},{280:325}))) 
gfs1m72=dim_avg_Wrap(dim_avg_Wrap(gfs_72(:,{-36:0},{280:325}))) 

print("america do sul")
;>>>>>>>>>>>>>>>>>>>>>>>>>>>>

;>>>>>>>>>>>>>>>Amazona (norte)
;media do observado
aa2o=dim_avg_Wrap(dim_avg_Wrap(tmpa(:,{-12:0},{295:310})))
;----- 24hrs
n2m24=dim_avg_Wrap(dim_avg_Wrap(new1_24(:,{-12:0},{295:310})))
aa2m24=dim_avg_Wrap(dim_avg_Wrap(new2_24(:,{-12:0},{295:310})))
gfs2m24=dim_avg_Wrap(dim_avg_Wrap(gfs_24(:,{-12:0},{295:310})))

;----- 48hrs
n2m48=dim_avg_Wrap(dim_avg_Wrap(new1_48(:,{-12:0},{295:310})))
aa2m48=dim_avg_Wrap(dim_avg_Wrap(new2_48(:,{-12:0},{295:310})))
gfs2m48=dim_avg_Wrap(dim_avg_Wrap(gfs_48(:,{-12:0},{295:310})))

;----- 72hrs
n2m72=dim_avg_Wrap(dim_avg_Wrap(new1_72(:,{-12:0},{295:310})))
aa2m72=dim_avg_Wrap(dim_avg_Wrap(new2_72(:,{-12:0},{295:310})))
gfs2m72=dim_avg_Wrap(dim_avg_Wrap(gfs_72(:,{-12:0},{295:310})))

print("Amazona NORTE OK")
;>>>>>>>>>>>>>>>>>>>>>>>>>>>

;>>>>>>>>>>>>>>>Nordeste
;media do observado
 aa3o=dim_avg_Wrap(dim_avg_Wrap(tmpa(:,{-12:0},{310:325})))
;----- 24hrs
n3m24=dim_avg_Wrap(dim_avg_Wrap(new1_24(:,{-12:0},{310:325})))
aa3m24=dim_avg_Wrap(dim_avg_Wrap(new2_24(:,{-12:0},{310:325})))
gfs3m24=dim_avg_Wrap(dim_avg_Wrap(gfs_24(:,{-12:0},{310:325})))

;----- 48hrs
n3m48=dim_avg_Wrap(dim_avg_Wrap(new1_48(:,{-12:0},{310:325})))
aa3m48=dim_avg_Wrap(dim_avg_Wrap(new2_48(:,{-12:0},{310:325})))
gfs3m48=dim_avg_Wrap(dim_avg_Wrap(gfs_48(:,{-12:0},{310:325})))

;----- 72hrs
n3m72=dim_avg_Wrap(dim_avg_Wrap(new1_72(:,{-12:0},{310:325})))
aa3m72=dim_avg_Wrap(dim_avg_Wrap(new2_72(:,{-12:0},{310:325})))
gfs3m72=dim_avg_Wrap(dim_avg_Wrap(gfs_72(:,{-12:0},{310:325})))

print("nordeste OK")            
;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

;>>>>>>>>>>>>>>Centro Oeste
;media do observado
aa4o=dim_avg_Wrap(dim_avg_Wrap(tmpa(:,{-24:-12},{295:310})))
;----- 24hrs
n4m24=dim_avg_Wrap(dim_avg_Wrap(new1_24(:,{-24:-12},{295:310})))
aa4m24=dim_avg_Wrap(dim_avg_Wrap(new2_24(:,{-24:-12},{295:310})))
gfs4m24=dim_avg_Wrap(dim_avg_Wrap(gfs_24(:,{-24:-12},{295:310})))

;----- 48hrs
n4m48=dim_avg_Wrap(dim_avg_Wrap(new1_48(:,{-24:-12},{295:310})))
aa4m48=dim_avg_Wrap(dim_avg_Wrap(new2_48(:,{-24:-12},{295:310})))
gfs4m48=dim_avg_Wrap(dim_avg_Wrap(gfs_48(:,{-24:-12},{295:310})))

;----- 72hrs
n4m72=dim_avg_Wrap(dim_avg_Wrap(new1_72(:,{-24:-12},{295:310})))
aa4m72=dim_avg_Wrap(dim_avg_Wrap(new2_72(:,{-24:-12},{295:310})))
gfs4m72=dim_avg_Wrap(dim_avg_Wrap(gfs_72(:,{-24:-12},{295:310})))
print("centro oeste OK")             
;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

;>>>>>>>>>>>>>>Sudeste nova area
;media do observado
 aa5o=dim_avg_Wrap(dim_avg_Wrap(tmpa(:,{-24:-15},{305:325})))           
;----- 24hrs
n5m24=dim_avg_Wrap(dim_avg_Wrap(new1_24(:,{-24:-15},{305:325})))       
aa5m24=dim_avg_Wrap(dim_avg_Wrap(new2_24(:,{-24:-15},{305:325})))      
gfs5m24=dim_avg_Wrap(dim_avg_Wrap(gfs_24(:,{-24:-15},{305:325})))      

;----- 48hrs
n5m48=dim_avg_Wrap(dim_avg_Wrap(new1_48(:,{-24:-15},{305:325})))       
aa5m48=dim_avg_Wrap(dim_avg_Wrap(new2_48(:,{-24:-15},{305:325})))      
gfs5m48=dim_avg_Wrap(dim_avg_Wrap(gfs_48(:,{-24:-15},{305:325})))      

;----- 72hrs
n5m72=dim_avg_Wrap(dim_avg_Wrap(new1_72(:,{-24:-15},{305:325})))       
aa5m72=dim_avg_Wrap(dim_avg_Wrap(new2_72(:,{-24:-15},{305:325}))) 
gfs5m72=dim_avg_Wrap(dim_avg_Wrap(gfs_72(:,{-24:-15},{305:325}))) 
print("sudeste nova area OK")
;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

;>>>>>>>>>>>>>Sudeste
;media do observado 
aa6o=dim_avg_Wrap(dim_avg_Wrap(tmpa(:,{-24:-12},{310:325})))
;---- 24 hrs
n6m24=dim_avg_Wrap(dim_avg_Wrap(new1_24(:,{-24:-12},{310:325})))
aa6m24=dim_avg_Wrap(dim_avg_Wrap(new2_24(:,{-24:-12},{310:325})))
gfs6m24=dim_avg_Wrap(dim_avg_Wrap(gfs_24(:,{-24:-12},{310:325})))

;---- 48 hrs
n6m48=dim_avg_Wrap(dim_avg_Wrap(new1_48(:,{-24:-12},{310:325})))
aa6m48=dim_avg_Wrap(dim_avg_Wrap(new2_48(:,{-24:-12},{310:325})))
gfs6m48=dim_avg_Wrap(dim_avg_Wrap(gfs_48(:,{-24:-12},{310:325})))

;---- 72 hrs
n6m72=dim_avg_Wrap(dim_avg_Wrap(new1_72(:,{-24:-12},{310:325})))
aa6m72=dim_avg_Wrap(dim_avg_Wrap(new2_72(:,{-24:-12},{310:325})))
gfs6m72=dim_avg_Wrap(dim_avg_Wrap(gfs_72(:,{-24:-12},{310:325})))

print("sudeste")             
;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

;>>>>>>>>>>>>>la plata
;media do observado
aa7o=dim_avg_Wrap(dim_avg_Wrap(tmpa(:,{-36:-24},{295:315})))
;---- 24hrs
n7m24=dim_avg_Wrap(dim_avg_Wrap(new1_24(:,{-36:-24},{295:315})))
aa7m24=dim_avg_Wrap(dim_avg_Wrap(new2_24(:,{-36:-24},{295:315})))
gfs7m24=dim_avg_Wrap(dim_avg_Wrap(gfs_24(:,{-36:-24},{295:315})))

;---- 48hrs
n7m48=dim_avg_Wrap(dim_avg_Wrap(new1_48(:,{-36:-24},{295:315})))
aa7m48=dim_avg_Wrap(dim_avg_Wrap(new2_48(:,{-36:-24},{295:315})))
gfs7m48=dim_avg_Wrap(dim_avg_Wrap(gfs_48(:,{-36:-24},{295:315})))

;---- 72hrs
n7m72=dim_avg_Wrap(dim_avg_Wrap(new1_72(:,{-36:-24},{295:315})))
aa7m72=dim_avg_Wrap(dim_avg_Wrap(new2_72(:,{-36:-24},{295:315})))
gfs7m72=dim_avg_Wrap(dim_avg_Wrap(gfs_72(:,{-36:-24},{295:315})))
print("la plata OK")
;>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

x1 = (/1,2,3,4/)

end 
