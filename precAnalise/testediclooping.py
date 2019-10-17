#config = {'Regiao': 'NORTE', 'Setor':'B7', 'latNorte':'2','latSul':'-11','lonOeste':'-75','lonLest':'-65'}

config = {
     'Regiao'  :['SUL' ,'SUDESTE'  ,'CENTRO-OESTE' ,'NORDESTE' ,'NORTE'    ,'SUDESTE'  ,'NORTE'    ],
     'Setor'   :['B1'  ,'B2'       ,'B3'           ,'B4'       ,'B5'       ,'B6'       ,'B7'       ],
     'latNorte':[156   ,170        ,169            ,3          ,2          ,-15        ,2          ],
     'latSul'  :[-35   ,-24        ,-35            ,-11        ,-11        ,-24        ,-11        ],
     'lonOeste':[-65   ,-49        ,-65            ,-51        ,-65        ,-51        ,-75        ],
     'lonLest' :[-49   ,-39        ,-49            ,-34        ,-49        ,-39        ,-65        ]
   }

for index in range(0,7,1):
    print(config['latNorte'][index] )



#set_extent([x0,x1,y0,y1])
#America do Sul
#set_extent([-82, -34, -50, 12])
#Norte B5
#ax.set_extent([-65, -49, -11, 2])
#Norte B7
#ax.set_extent([-75, -65, -11, 2])
#Nordeste B4
#ax.set_extent([-51, -34, -11, 3])
#Centro-Oeste B3
#ax.set_extent([-65, -49, -35, -11])
#Sul B1
#ax.set_extent([-65, -49, -35, -24])
#Sudeste B2
#ax.set_extent([-49, -39, -24, -10])
#Sudeste B6
#ax.set_extent([-51, -39, -24, -15])