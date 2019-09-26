;================================================;
;  maponly_16.ncl
;================================================;

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"      ; These four libraries are automatically
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"       ; loaded from NCL V6.4.0 onward.
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"   ; No need for user to explicitly load.
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begin 

  wks = gsn_open_wks("png","maponly")      ; send graphics to PNG file
  gsn_define_colormap(wks,"amwg")

plot = new(2,graphic)

  res                       = True  
  res@gsnDraw             = False
  res@gsnFrame            = False 
  res@gsnMaximize           = False ; True         ; Maximize plot in frame.
  res@mpCenterLonF= 180
  res@mpDataBaseVersion    = "HighRes"
  res@gsnPaperOrientation   = "Portrait"
  res@pmTickMarkDisplayMode = "Always"     ; Turn on map tickmarks
  res@mpDataSetName         = "Earth..4"   ; This new database contains
  ;res@mpDataBaseVersion     = "MediumRes"  ; Medium resolution database
  res@mpOutlineOn           = True         ; Turn on map outlines
  res@mpOutlineSpecifiers   = (/"Brazil:states"/) 
  res@mpFillOn              = True         ; Turn on map fill
  res@mpFillBoundarySets    = "National"
  res@mpFillAreaSpecifiers  = (/"Brazil:states"/)
  res@tiMainString          = "States of Brazil"
  res@mpMaxLatF             =  15          ;  South America limits 
  res@mpMinLatF             = -57
  res@mpMaxLonF             = 330
  res@mpMinLonF             = 270
  res@tiMainOffsetYF = -0.02          ;reduz o espaÃ§o entre o titulo e a imagem
  res@tiMainFontHeightF   = 0.02   
  res@tiMainString = "South America"
  ;res@gsnLeftString         = "Versao "

;;Draw a text string at the bottom
;  txres               = True
;  txres@txFontHeightF = 0.015
;  gsn_text_ndc(wks,"Figure : Global Forecast System (GFS)",0.5,0.15,txres)
;
plot(0) = gsn_csm_map(wks,res)

      txres               = True
      txres@txFontHeightF = 0.015
      gsn_text_ndc(wks,"Figure : Map of South America",0.5,0.15,txres)
      res@mpDataBaseVersion     = "MediumRes"  ; Medium resolution database
plot(1) = gsn_csm_map(wks,res)

;##Plot 00003

;************************************************
; create panel
;************************************************
      resP                    = True                 ; modify the panel plot
      resP@gsnMaximize          =  False ; True 

      gsn_panel(wks,plot,(/1,1/),resP)               ; now draw as one plot


;************************************************
; create parameters
;************************************************

draw(plot)
  ;  drawNDCGrid(wks)
      txres               = True
      txres@txFontHeightF = 0.011
     
      gsn_text_ndc(wks,"Figure : Map of South America ",0.5,0.18,txres)

      txres@txFont = "helvetica-bold"
      txres@txBackgroundFillColor = "White"
      txres@txPerimOn = True
      ;#B1 B2 B3 B4 B5 B6
      gsn_text_ndc(wks,"B1",0.478,0.465,txres) ;OK 
      gsn_text_ndc(wks,"B2",0.59,0.564,txres)  ;OK
      gsn_text_ndc(wks,"B3",0.478,0.564,txres) ;OK 
      gsn_text_ndc(wks,"B4",0.59,0.633,txres)
      gsn_text_ndc(wks,"B5",0.528,0.670,txres) ;OK
      gsn_text_ndc(wks,"B6",0.563,0.53,txres)
      gsn_text_ndc(wks,"B7",0.405,0.660,txres) ;OK

      ;#Estados do Brasil
      delete(txres@txBackgroundFillColor)
      delete(txres@txPerimOn)
      txres@txFontHeightF = 0.007 
      txres@txFont = "helvetica"
      gsn_text_ndc(wks,"SP",0.585,0.49,txres) ;OK 
      gsn_text_ndc(wks,"MG",0.61,0.51,txres) ;OK 
      gsn_text_ndc(wks,"ES",0.64,0.51,txres) ;OK 
      gsn_text_ndc(wks,"RJ",0.63,0.492,txres) ;OK 
      
      gsn_text_ndc(wks,"AC",0.435,0.58,txres) ;OK 
      gsn_text_ndc(wks,"RO",0.478,0.583,txres) ;OK 
      gsn_text_ndc(wks,"PA",0.545,0.623,txres) ;OK 
      gsn_text_ndc(wks,"AM",0.485,0.623,txres) ;OK 
      gsn_text_ndc(wks,"RR",0.49,0.67,txres) ;OK 
      gsn_text_ndc(wks,"AP",0.56,0.662,txres) ;OK 
      gsn_text_ndc(wks,"TO",0.585,0.585,txres) ;OK 


      gsn_text_ndc(wks,"MT",0.535,0.553,txres) ;ok
      gsn_text_ndc(wks,"MS",0.535,0.51,txres) ;ok
      gsn_text_ndc(wks,"GO",0.585,0.535,txres) ;OK 
      
      gsn_text_ndc(wks,"MA",0.61,0.61,txres) ;OK 
      gsn_text_ndc(wks,"PI",0.63,0.6,txres) ;OK 
      gsn_text_ndc(wks,"CE",0.648,0.615,txres) ;OK 
      gsn_text_ndc(wks,"RN",0.7,0.62,txres) ;OK 
      gsn_text_ndc(wks,"PB",0.7,0.605,txres) ;OK 
      gsn_text_ndc(wks,"PE",0.7,0.593,txres) ;OK
      gsn_text_ndc(wks,"AL",0.7,0.58,txres) ;OK
      gsn_text_ndc(wks,"SE",0.7,0.565,txres) ;OK
      gsn_text_ndc(wks,"BA",0.63,0.56,txres) ;OK 

      gsn_text_ndc(wks,"RS",0.545,0.44,txres) ;OK 
      gsn_text_ndc(wks,"SC",0.568,0.455,txres) ;OK 
      gsn_text_ndc(wks,"PR",0.562,0.469,txres) ;OK 



;#<><><><><><><><><><><><><teste linha
    ret = True
    ret@gsLineColor       = "black"                 ; color of lines
    ret@gsLineThicknessF  = 2.5 
    ;#> RN
    cirx6 = (/ .670, .670, .670, .670,  .69/)
    ciry6 = (/ .61, .61, .61, .61,  .62 /)
    gsn_polyline_ndc(wks,cirx6,ciry6,ret)  ; retangulo legend

    ;#> PB
    cirx6 = (/ .670, .670, .670, .670,  .69/)
    ciry6 = (/ .60, .60, .60, .60,  .605 /)
    gsn_polyline_ndc(wks,cirx6,ciry6,ret)  ; retangulo legend

     ;#> PE
    cirx6 = (/ .670, .670, .670, .670,  .69/)
    ciry6 = (/ .59, .59, .59, .59,  .593 /)
    gsn_polyline_ndc(wks,cirx6,ciry6,ret)  ; retangulo legend

      ;#> AL
    cirx6 = (/ .670, .670, .670, .670,  .69/)
    ciry6 = (/ .58, .58, .58, .58,  .58 /)
    gsn_polyline_ndc(wks,cirx6,ciry6,ret)  ; retangulo legend

       ;#> SE
    cirx6 = (/ .660, .660, .660, .660,  .69/)
    ciry6 = (/ .575, .575, .575, .575,  .568 /)
    gsn_polyline_ndc(wks,cirx6,ciry6,ret)  ; retangulo legend



      
    ;#Retangulo
    ret = True             ; Indicate you want to set some resources.
    ret@gsLineColor       = "black"                 ; color of lines
    ret@gsLineThicknessF  = 3.8 
    ;#Retangulo B1
    ;cirx = (/ .638, .500, .500, .638,  .638/)
    cirx = (/ .575, .465, .465, .575,  .575/)
    ciry = (/ .475, .475, .385, .385,  .475 /)
    gsn_polyline_ndc(wks,cirx,ciry,ret)  ; retangulo legend
    ;#Retangulo B2 ok 
    cirx2 = (/ .663, .575, .575, .663,  .663/)
    ciry2 = (/ .575, .575, .475, .475,  .575 /)
    gsn_polyline_ndc(wks,cirx2,ciry2,ret)  ; retangulo legend
    ;#Retangulo B3 ok
    cirx3 = (/ .575, .465, .465, .575,  .575/)
    ciry3 = (/ .575, .575, .475, .475,  .575 /)
    gsn_polyline_ndc(wks,cirx3,ciry3,ret)  ; retangulo legend
     ;#Retangulo B4 ok
    cirx4 = (/ .685, .575, .575, .685,  .685/)
    ciry4 = (/ .575, .575, .644, .644,  .575 /)
    gsn_polyline_ndc(wks,cirx4,ciry4,ret)  ; retangulo legend
    ;#Retangulo B5 ok
    cirx5 = (/ .575, .465, .465, .575,  .575/)
    ciry5 = (/ .682, .682, .575, .575,  .682 /)
    gsn_polyline_ndc(wks,cirx5,ciry5,ret)  ; retangulo legend
    delete(ret@gsLineColor)
    ;#Retangulo B7 ok
    ret@gsLineColor       = "red"
    cirx5 = (/ .465, .391, .391, .465,  .465/)
    ciry5 = (/ .670, .670, .568, .568,  .670 /)
    gsn_polyline_ndc(wks,cirx5,ciry5,ret)  ; retangulo legend
    ;#Retangulo B6 ok
    cirx6 = (/ .655, .550, .550, .655,  .655/)
    ciry6 = (/ .543, .543, .475, .475,  .543 /)
    ret@gsLineColor       = "red"
    gsn_polyline_ndc(wks,cirx6,ciry6,ret)  ; retangulo legend

    



frame(wks)

end 
