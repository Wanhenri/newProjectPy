

############################ EM CONSTRUÇÃO

def bias(predict, actual):
    difference = actual - predict 
    score = difference.mean()     
    return score

def rmse(predict, actual):

    difference = predict - actual
    square_diff = np.square(difference)
    mean_square_diff = square_diff.mean()
    score = np.sqrt(mean_square_diff)
    return score

def mae(predict, actual):
    difference = abs(actual - predict) 
    score = difference.mean()     
    return score





    config = {
      'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
      'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
      'latNorte':[ 75   ,130        ,130            ,195        ,195        ,130        ,195        ],
      'latSul'  :[-182  ,-119       ,-119           ,-45        ,-45        ,-139       ,-45        ],
      'lonOeste':[-157  ,-78        ,-157           ,-79        ,-157       ,-78        ,-210       ],
      'lonLest' :[-69   ,-1         ,-79            ,-1         ,-79        ,-1        ,-153        ]
    }


    for ind in range(0,7,1):
        print('ind',ind)

        for indVars in range(0,5,1):
            print('indVars',indVars)

        #for ind in range(0,7,1):
        #    print('ind',ind)

            pylab.rcParams['figure.figsize'] = (30,10)

            anomes = '201401'
            path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
            name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

            path_3 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
            name_file_3 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'

            path_4 = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
            name_file_4 = 'prev.2014.jan_12z_'+ prev +'h_interp.nc'

            path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"   

            latNorte    = config['latNorte'][ind]
            latSul      = config['latSul'][ind]
            lonOeste    = config['lonOeste'][ind]
            lonLest     = config['lonLest'][ind]


            DS_NCEP = xr.open_dataset(path_1 + name_file_1)
            DS_NCEP_umidade_nova = xr.open_dataset(path_3 + name_file_3)
            GFS = xr.open_dataset(path_4 + name_file_4)

            vars = {
            'ds':[
                DS_NCEP.prec              
                ,DS_NCEP.cssf               
                ,DS_NCEP.clsf               
                ,DS_NCEP.t2mt               
                ,DS_NCEP.q2mt   ],
            'ds_nova_umidade':[
                DS_NCEP_umidade_nova.prec 
                ,DS_NCEP_umidade_nova.cssf  
                ,DS_NCEP_umidade_nova.clsf  
                ,DS_NCEP_umidade_nova.t2mt  
                ,DS_NCEP_umidade_nova.q2mt],
            'ds_GFS': [
                GFS.APCP_surface
                ,GFS.SHTFL_surface
                ,GFS.LHTFL_surface
                ,GFS.TMP_2maboveground
                ,GFS.SPFH_2maboveground
            ],
            'variavel':[
                'PREC'                       
                ,'CSSF'                     
                ,'CLSF'                     
                ,'T2MT'                     
                ,'Q2MT'       ]
            }
    for previsao in range(24,192,24):
        prev = str(previsao)
        print(prev)
        path_1 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_GL/"
        name_file_1 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
        path_2 = "/dados/dmdpesq/Experimento_umidade_do_solo/MERGE/"
        name_file_2 = 'prec_'+anomes+'.nc'
        path_3 = "/dados/dmdpesq/Experimento_umidade_do_solo/umidade_Nova/"
        name_file_3 = 'JAN2014_'+ prev +'Z_12Z_interp.nc'
        path_4 = "/dados/dmdpesq/Experimento_umidade_do_solo/GFS/"    
        name_file_4 = 'prev.2014.jan.'+ prev +'h_interp.nc'
        path_out ="/dados/dmdpesq/Experimento_umidade_do_solo/out/"  


        latNorte    = config['latNorte'][ind]
        latSul      = config['latSul'][ind]
        lonOeste    = config['lonOeste'][ind]
        lonLest     = config['lonLest'][ind]

        DS_NCEP = xr.open_dataset(path_1 + name_file_1)

        longName = DS_NCEP.prec.attrs['long_name']


            #umidadeGL = DS_NCEP.prec.isel(time=slice(None, 31), lat=slice(2,-11), lon=slice(-75,-65)).mean(dim="lat").mean(dim="lon")

        umidadeGL = DS_NCEP.prec.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")

        DS_NCEP_umidade_nova = xr.open_dataset(path_3 + name_file_3)
        umidadeNova = DS_NCEP_umidade_nova.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).prec.mean(dim="lat").mean(dim="lon")

        GFS = xr.open_dataset(path_4 + name_file_4)
        modeloGFS = GFS.APCP_surface.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")
    #
        MERGE = xr.open_dataset(path_2 + name_file_2)
        obs = MERGE.prec.isel(time=slice(None, 31), lat=slice(latNorte,latSul), lon=slice(lonOeste,lonLest)).mean(dim="lat").mean(dim="lon")

        previsao = prev

        bias_umidadeGL = bias(obs, umidadeGL)
        bias_umidadeNova = bias(obs, umidadeNova)
        bias_modeloGFS = bias(obs, modeloGFS)

        lista_previsao.append(previsao)
        lista_bias_umidadeGL.append(bias_umidadeGL)
        lista_bias_umidadeNova.append(bias_umidadeNova)
        lista_bias_modeloGFS.append(bias_modeloGFS)
