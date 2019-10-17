load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "./read-data-br-series.ncl"


begin

;>>>PLOT 24<<<<<
;>>>>>data  plot 24hr
;>America do Sul
 data1      = new((/4,dimsizes(n1m24)/),double)
 data1(0,:) = n1m24   ;>>>SMG 
 data1(1,:) = aa1m24  ;>>>NCEP        
 data1(2,:) = aa1o    ;>>>IMERG        
 data1(3,:) = gfs1m24 ;>>>GFS         

;>Amazona (norte)
 data2      = new((/4,dimsizes(n1m24)/),double)
 data2(0,:) = n2m24   ;>>>SMG  
 data2(1,:) = aa2m24  ;>>>NCEP                       
 data2(2,:) = aa2o    ;>>>IMERG                       
 data2(3,:) = gfs2m24 ;>>>GFS         

;>Nordeste
 data3      = new((/4,dimsizes(n1m24)/),double)
 data3(0,:) = n3m24   ;>>>SMG  
 data3(1,:) = aa3m24  ;>>>NCEP                     
 data3(2,:) = aa3o    ;>>>IMERG                    
 data3(3,:) = gfs3m24 ;>>>GFS         

;>Centro Oeste
 data4      = new((/4,dimsizes(n1m24)/),double)
 data4(0,:) = n4m24   ;>>>SMG   
 data4(1,:) = aa4m24  ;>>>NCEP                    
 data4(2,:) = aa4o    ;>>>IMERG 
 data4(3,:) = gfs4m24 ;>>>GFS                    

;>Sudeste nova area
 data5      = new((/4,dimsizes(n1m24)/),double)
 data5(0,:) = n5m24   ;>>>SMG   
 data5(1,:) = aa5m24  ;>>>NCEP                    
 data5(2,:) = aa5o    ;>>>IMERG                    
 data5(3,:) = gfs5m24 ;>>>GFS 

;>Sudeste
 data6      = new((/4,dimsizes(n1m24)/),double)
 data6(0,:) = n6m24   ;>>>SMG  
 data6(1,:) = aa6m24  ;>>>NCEP                    
 data6(2,:) = aa6o    ;>>>IMERG                    
 data6(3,:) = gfs6m24 ;>>>GFS 

;>la plata
 data7      = new((/4,dimsizes(n1m24)/),double)
 data7(0,:) = n7m24   ;>>>SMG  
 data7(1,:) = aa7m24  ;>>>NCEP                   
 data7(2,:) = aa7o    ;>>>IMERG                   
 data7(3,:) = gfs7m24 ;>>>GFS 
;*
;*
;*
;>>>PLOT 48<<<<<
;>>>>>data  plot 48hr
;>America do Sul
 data8      = new((/4,dimsizes(n1m24)/),double)
 data8(0,:) = n1m48   ;>>>SMG 
 data8(1,:) = aa1m48  ;>>>NCEP  
 data8(2,:) = aa1o    ;>>>IMERG
 data8(3,:) = gfs1m48 ;>>>GFS   

;>Amazona (norte)
 data9      = new((/4,dimsizes(n1m24)/),double)
 data9(0,:) = n2m48   ;>>>SMG  
 data9(1,:) = aa2m48  ;>>>NCEP                       
 data9(2,:) = aa2o    ;>>>IMERG                       
 data9(3,:) = gfs2m48 ;>>>GFS 

;>Nordeste
 data10      = new((/4,dimsizes(n1m24)/),double)
 data10(0,:) = n3m48   ;>>>SMG  
 data10(1,:) = aa3m48  ;>>>NCEP                     
 data10(2,:) = aa3o    ;>>>IMERG                     
 data10(3,:) = gfs3m48  ;>>>GFS 

;>Centro Oeste
 data11      = new((/4,dimsizes(n1m24)/),double)
 data11(0,:) = n4m48   ;>>>SMG   
 data11(1,:) = aa4m48  ;>>>NCEP                    
 data11(2,:) = aa4o    ;>>>IMERG                    
 data11(3,:) = gfs4m48 ;>>>GFS 

;>Sudeste nova area
 data12      = new((/4,dimsizes(n1m24)/),double)
 data12(0,:) = n5m48   ;>>>SMG   
 data12(1,:) = aa5m48  ;>>>NCEP                    
 data12(2,:) = aa5o    ;>>>IMERG                    
 data12(3,:) = gfs5m48 ;>>>GFS 

;>Sudeste
 data13      = new((/4,dimsizes(n1m24)/),double)
 data13(0,:) = n6m48   ;>>>SMG  
 data13(1,:) = aa6m48  ;>>>NCEP                    
 data13(2,:) = aa6o    ;>>>IMERG  
 data13(3,:) = gfs6m48 ;>>>GFS                   

;>la plata
 data14      = new((/4,dimsizes(n1m24)/),double)
 data14(0,:) = n7m48   ;>>>SMG  
 data14(1,:) = aa7m48  ;>>>NCEP   
 data14(2,:) = aa7o    ;>>>IMERG
 data14(3,:) = gfs7m48 ;>>>GFS    
;*
;*
;*
;>>>PLOT 72<<<<<
;>>>>>data  plot 72hr
;>America do Sul
 data15      = new((/4,dimsizes(n1m24)/),double)
 data15(0,:) = n1m72   ;>>>SMG 
 data15(1,:) = aa1m72  ;>>>NCEP        
 data15(2,:) = aa1o    ;>>>IMERG        
 data15(3,:) = gfs1m72 ;>>>GFS 

;>Amazona (norte)
 data16      = new((/4,dimsizes(n1m24)/),double)
 data16(0,:) = n2m72   ;>>>SMG  
 data16(1,:) = aa2m72  ;>>>NCEP                       
 data16(2,:) = aa2o    ;>>>IMERG                       
 data16(3,:) = gfs2m72 ;>>>GFS 

;>Nordeste
 data17      = new((/4,dimsizes(n1m24)/),double)
 data17(0,:) = n3m72   ;>>>SMG  
 data17(1,:) = aa3m72  ;>>>NCEP                     
 data17(2,:) = aa3o    ;>>>IMERG
 data17(3,:) = gfs3m72 ;>>>GFS                      

;>Centro Oeste
 data18      = new((/4,dimsizes(n1m24)/),double)
 data18(0,:) = n4m72   ;>>>SMG   
 data18(1,:) = aa4m72  ;>>>NCEP                    
 data18(2,:) = aa4o    ;>>>IMERG 
 data18(3,:) = gfs4m72 ;>>>GFS                    

;>Sudeste nova area
 data19      = new((/4,dimsizes(n1m24)/),double)
 data19(0,:) = n5m72   ;>>>SMG   
 data19(1,:) = aa5m72  ;>>>NCEP                    
 data19(2,:) = aa5o    ;>>>IMERG                    
 data19(3,:) = gfs5m72 ;>>>GFS 

;>Sudeste
 data20      = new((/4,dimsizes(n1m24)/),double)
 data20(0,:) = n6m72   ;>>>SMG  
 data20(1,:) = aa6m72  ;>>>NCEP                    
 data20(2,:) = aa6o    ;>>>IMERG 
 data20(3,:) = gfs6m72 ;>>>GFS                    

;>la plata
 data21      = new((/4,dimsizes(n1m24)/),double)
 data21(0,:) = n7m72   ;>>>SMG  
 data21(1,:) = aa7m72  ;>>>NCEP   
 data21(2,:) = aa7o    ;>>>IMERG   
 data21(3,:) = gfs7m72 ;>>>GFS

tm=fall2->time

print("tm")
printVarSummary(tm)

wks = gsn_open_wks( "ps", "teste" )

plot_L = new(21,graphic)

;----------------------------------------------------------------
;  plots  --> 
;----------------------------------------------------------------
  op                           = True
  op@trXMinF                   =tm(0);>>> 0; 1456833600;1456833600; 0
  op@trXMaxF                   =tm(24) ;>>>tm(89);
  op@trYMinF                   = 0; 2.4 
  op@trYMaxF                   = 25 ;>>25 ;>>>>20 ;>>>40;30 ;5.6 
  op@gsnDraw                   = False
  op@gsnFrame                  = False
  
;>>>op@xyDashPatterns            = (/0,1,0,2,2/)                           ; Make curves all solid
  op@xyDashPatterns            = (/0,1,0,0/) 

  op@xyMarkLineMode            = "Lines"                     ; Markers *and* lines
  op@xyLineThicknessF          = 0.5
  op@xyLineColors              = (/"orange","purple","black","forestgreen"/);>>>,"white","white","white","white"/) ;>>>>(/"black","black","black","black","orange","purple"/) ;line color
  op@tmXBMajorThicknessF       = 0.8
  op@tmYLMajorThicknessF       = 0.8
  op@tmXBLabelConstantSpacingF = 1.5
  op@tmXBMajorLengthF          = 0.0001
  op@tmYRMinorOn               = False                                      ; Turn off left minor tickmarks
  op@tmXTOn                    = False                                      ; Turn off top tickmarks
  op@tmYROn                    = False                                      ; Turn off top tickmarks
  op@tmXBMinorOn               = True    
  op@tmYRBorderOn              = True                                       ; turn off right axis
  op@tmXBMajorOutwardLengthF   = 0.009
  op@tmXBMajorLengthF          = 0.004
  op@tmBorderThicknessF        = 0.5
  op@tmXTBorderOn              = True                                       ; turn off right axis
  op@tmXBBorderOn              = True                                       ; turn off right axis
  op@tmXBMode                  = "Explicit" 
  op@tmXBLabelFontHeightF      = 0.0125
  op@tmXBLabelStride           = 1
  op@tmXBLabelAngleF           = 45          ; change label angle
  op@tmXBValues                = tm(0:24) ; tm(0:89) 
  ;>>>>legenda iniciando no dia primeiro
  ;op@tmXBLabels                = (/" "," "," "," ","5"," "," "," "," ","10"," "," "," "," ","15" \
  ;                                ," "," "," "," ","20"," "," "," "," ","25"," "," "," "," ","30"," " \
  ;                                , " "," "," ","35"," "," "," "," ","40"," "," "," "," ","45"," " \
  ;                                ," "," "," ","50"," "," "," "," ","55"," "," "," "," ","60"," "," " \
  ;                              ," "," ","65"," "," "," "," ","70"," "," "," "," ","75"," "," "," " \
  ;                                ," ","80"," "," "," "," ","85"," "," "," "," ","90"," "," "/)
  ;>>>>>legenda iniciando no dia 5
  op@tmXBLabels                = (/"5"," "," "," ","10"," "," "," "," ","15"," "," "," "," ","20" \
                                  ," "," "," "," ",""," "," "," "," ","25"," "," "," "," ","30"," " \
                                  , " "," "," ","35"," "," "," "," ","40"," "," "," "," ","45"," " \
                                  ," "," "," ","50"," "," "," "," ","55"," "," "," "," ","60"," "," " \
                                  ," "," ","65"," "," "," "," ","70"," "," "," "," ","75"," "," "," " \
                                  ," ","80"," "," "," "," ","85"," "," "," "," ","90"," "," "/)




  op@tmXBLabelJust             = "BottomRight"
  op@vpWidthF                  = 0.8                                       ; Set width and height of plot.
  op@vpHeightF                 = 0.4
  op@lgItemOrder               = (/3,2,1,0/)               ; reverse legend



;;>>>>>>add a legend<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  op@pmLegendDisplayMode       = "Always"              ; turn on legend
  op@pmLegendSide              = "Top"                 ; Change location of
  op@pmLegendParallelPosF      = .80;                  ; move units right
  op@pmLegendOrthogonalPosF    = -.33                  ; more neg = down
  op@pmLegendWidthF            = 0.08                   ; Change width and
  op@pmLegendHeightF           = 0.13                  ; height of legend.
  op@lgLabelFontHeightF        = .018                  ; change font height
  op@lgPerimOn                 = False                 ; no box around
  op@lgLabelFont               = "helvetica-bold"
  op@xyExplicitLegendLabels    =(/"BAM-DAS", "BAM","IMERG","GFS"/);>>>," "," "," "," "/) 

;>>>>>>>>>>>>>> plots 

;>>>>>>plot - AREA - La Plata - INICIO

  ;  op@trYMinF                 = 2
  ;  op@trYMaxF                 = 3

  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  op@tiYAxisString             = "Precipitation (mm/day)"
  plot_L(0)=gsn_csm_xy(wks,tm,data7,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(1)=gsn_csm_xy(wks,tm,data14,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(2)=gsn_csm_xy(wks,tm,data21,op)

  ;delete(op@trYMinF)
  ;delete(op@trYMaxF)

  ;op@trYMinF                   = 0
  ;op@trYMaxF                   = 14


;>>>>>plot - AREA - La Plata - FIM 

;>>>>>plot - AREA - Sudeste - INICIO

  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  op@tiYAxisString          = "Precipitation (mm/day)"
  plot_L(3)=gsn_csm_xy(wks,tm,data6,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  plot_L(4)=gsn_csm_xy(wks,tm,data13,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(5)=gsn_csm_xy(wks,tm,data20,op)

;>>>>>>>>plot - AREA - Sudeste - FIM

;>>>>>>>>plot - AREA - Nova area Sudeste - INICIO

  op@tiYAxisString          = "Precipitation (mm/day)"
  plot_L(6)=gsn_csm_xy(wks,tm,data5,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  plot_L(7)=gsn_csm_xy(wks,tm,data12,op)
  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(8)=gsn_csm_xy(wks,tm,data19,op)

;>>>>>>>plot - AREA - Nova area Sudeste - FIM

;>>>>>>>plot - AREA - Centro Oeste - INICIO

  op@tiYAxisString          = "Precipitation (mm/day)"
  plot_L(9)=gsn_csm_xy(wks,tm,data4,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  plot_L(10)=gsn_csm_xy(wks,tm,data11,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(11)=gsn_csm_xy(wks,tm,data18,op)

;>>>>>>>plot - AREA - Centro Oeste - FIM

;>>>>>>>plot - AREA - Nordeste - INICIO

  op@tiYAxisString          = "Precipitation (mm/day)"
  plot_L(12)=gsn_csm_xy(wks,tm,data3,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  plot_L(13)=gsn_csm_xy(wks,tm,data10,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(14)=gsn_csm_xy(wks,tm,data17,op)

;>>>>>>>plot - AREA - Nordeste - FIM

;>>>>>>>plot - AREA - Amazonas (norte) - INICIO

  op@tiYAxisString          = "Precipitation (mm/day)"
  plot_L(15)=gsn_csm_xy(wks,tm,data2,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  plot_L(16)=gsn_csm_xy(wks,tm,data9,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(17)=gsn_csm_xy(wks,tm,data16,op)

;>>>>>>plot - AREA - Amazonas (Norte) - FIM

;>>>>>>plot - AREA - america do sul - INICIO

  op@tiYAxisString          = "Precipitation (mm/day)"
  op@tiXAxisString          = "Days (from May 2015)"
  plot_L(18)=gsn_csm_xy(wks,tm,data1,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  plot_L(19)=gsn_csm_xy(wks,tm,data8,op)

  delete(op@tiYAxisString)
  op@tiYAxisString          = " "
  op@pmLegendDisplayMode    = "Always"              ; turn on legend
  plot_L(20)=gsn_csm_xy(wks,tm,data15,op)

;>>>>>>>plot - AREA - America do sul - FIM

;>>>>>>>drawNDCGrid(wks)


;************************************************
; Attach text to plot using plot coordinates.
;************************************************
  txres1 = True                     ; text mods desired
  txres1@txFontHeightF = 0.002
  txres1@txPerimOn = False          ;True
  txres1@txFont = "helvetica-bold"

  h=(/"24 h"/)
  ;>x=(/0.449/)
  x=(/0.400/)
  y=(/0.993/)

  gsn_text_ndc(wks,h,x,y(:),txres1)

  h=(/"48 h"/)
  ;>x=(/0.533/)   
  x=(/0.490/)   
  y=(/0.993/)     

 gsn_text_ndc(wks,h,x,y(:),txres1)

  h=(/"72 h"/)
  ;>x=(/0.619/) 
  x=(/0.577/) 
  y=(/0.993/)


  gsn_text_ndc(wks,h,x,y(:),txres1)

;nome da estacao
  h=(/" "/)
  x=(/0.449/)
  y=(/0.989/)
 gsn_text_ndc(wks,h,x,y(:),txres1)


 h=(/" "/)
 x=(/0.533/) 
 y=(/0.989/)
 gsn_text_ndc(wks,h,x,y(:),txres1)


  h=(/" "/)
  x=(/0.619/) 
  y=(/0.989/)
  gsn_text_ndc(wks,h,x,y(:),txres1)

;************************************************
; create panel 
;************************************************
  resPanel                                  = True                 ; panel mods desired
  resPanel@gsnFrame                         = True ;False
  resPanel@gsnPanel                         = 0.5
  resPanel@amJust                           = "TopRight" ;"TopLeft";
  resPanel@amParallelPosF                   = -0.05                ;move right left
  resPanel@amOrthogonalPosF                 = -0.49 ; 35                 ;move up down
  resPanel@gsnPanelFigureStringsFontHeightF = 0.002;0.003;0.005                ; make small
  resPanel@gsnPanelFigureStringsPerimOn     = False
  resPanel@gsnPanelFigureStrings            = (/"a) La Plata (B1)        ", "a') La Plata (B1)     ","a') La Plata (B1)     ", \
                                                "b) Southeast (B2)     ", "b') Southeast (B2)    ","b') Southeast (B2)    " , \
                                                "b) Novo-Southeast (B6)     ", "b') Novo-Southeast (B6)    ","b') Novo-Southeast (B6)    " , \
                                                "c) Central-West (B3) ", "c') Central-West (B3)","c') Central-West (B3)", \
                                                "d) Northeast (B4)     ", "d') Northeast (B4)    ","d') Northeast (B4)     ",\
                                                "e) Amazon (B5)        ", "e') Amazon (B5)       ", "e') Amazon (B5)       ",\
                                                "f) America do Sul        ", "f')America do Sul       ", "f')America do Sul        "/)

  resPanel@gsnPanelXWhiteSpacePercent = 0.0
  resPanel@gsnPanelYWhiteSpacePercent = 1.5

  gsn_panel(wks,plot_L,(/21,3/),resPanel)
  delete(wks)

  system("convert -trim -density 600 -rotate -360 teste.ps teste.png ; rm teste.ps")


end
