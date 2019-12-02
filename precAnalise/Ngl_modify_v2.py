import numpy
import Ngl

def taylor_diagram(wks, RATIO, CC, rOpts):
  
  dimR                  = RATIO.shape
  nCase                 = dimR[0]                   # # of cases [models] 
  nVar                  = dimR[1]                   # # of variables

                                                    # x/y coordinates for plotting
  X    = numpy.zeros( (nCase,nVar) , dtype=RATIO.dtype )
  Y    = numpy.zeros( (nCase,nVar) , dtype=RATIO.dtype )

  for nc in range(nCase):
     angle      = numpy.arccos( CC[nc,:] )             # array operation                                    
     X[nc,:]    = RATIO[nc,:] * numpy.cos( angle )     
     Y[nc,:]    = RATIO[nc,:] * numpy.sin( angle )    

  xyMin                 = 0
  xyOne                 = 1.00
  xyMax                 = 1.65
  xyMax_Panel           = xyMax+ 0.10                # paneling purposes
 
  if (rOpts and hasattr(rOpts,"txFontHeightF"))  : 
      FontHeightF       = rOpts.txFontHeightF        # user wants to specify size
  else :
      FontHeightF       = 0.0175
 
# ----------------------------------------------------------------
# Part 1:
# base plot: Based upon request of Mark Stevens
# basic x-y and draw the 1.0 observed and the outer curve at 1.65
# ----------------------------------------------------------------
  
  rxy = Resources() 
  rxy.nglDraw           = False
  rxy.nglFrame          = False
  rxy.vpHeightF         = 0.65
  rxy.vpWidthF          = 0.65
  rxy.tmYLBorderOn      = False
  rxy.tmXBBorderOn      = False

  rxy.tiYAxisString     = "Standardized Deviations (Normalized)"
  rxy.tiYAxisFontHeightF= FontHeightF                # default=0.025 
  
  rxy.tmXBMode          = "Explicit" 
  rxy.tmXBValues        = [0.0,0.25,0.50,0.75,1.00,1.25,1.5]    # major tm
  rxy.tmXBLabels        = ["    ","0.25","0.50","0.75","REF" ,"1.25","1.50"]
  if (rOpts and hasattr(rOpts,"OneX") )  :           # eg: rOpts.OneX="1.00" 
      rxy.tmXBLabels        = ["    ","0.25","0.50","0.75",rOpts.OneX,"1.25","1.50"]

  rxy.tmXBMajorLengthF  = 0.015                      # default=0.02 for a vpHeightF=0.6
  rxy.tmXBLabelFontHeightF = FontHeightF
  rxy.tmXBMinorOn       = False
  rxy.trXMaxF           = xyMax_Panel

  rxy.tmYLMode          = "Manual"
  rxy.tmYLMinorOn       = False
  rxy.tmYLMajorLengthF  = rxy.tmXBMajorLengthF
  rxy.tmYLLabelFontHeightF = FontHeightF
  rxy.tmYLMode          = "Explicit" 
  rxy.tmYLValues        = [0.0, .25, 0.50, 0.75, 1.00, 1.25, 1.5] # major tm
  rxy.tmYLLabels        = ["0.00","0.25","0.50","0.75","1.00","1.25","1.50"]
  rxy.trYMaxF           = xyMax_Panel

  rxy.tmYRBorderOn      = False
  rxy.tmYROn            = False      # Turn off right tick marks.

  rxy.tmXTBorderOn      = False
  rxy.tmXTOn            = False      # Turn off right tick marks.

  rxy.xyDashPatterns    = [ 0 ]      # line characteristics (dash,solid)
  rxy.xyLineThicknesses = [ 2.]      # choose line thickness

  rxy.nglFrame          = False      # Don't advance the frame.

                                     # create outer 'correlation axis'
  npts    = 200                      # arbitrary
  xx      = numpy.linspace(xyMin,xyMax,npts) 
  yy      = numpy.sqrt(xyMax**2 - xx**2    )   # outer correlation line (xyMax)

  sLabels = ["0.0","0.1","0.2","0.3","0.4","0.5","0.6",    # correlation labels
             "0.7","0.8","0.9","0.95","0.99","1.0"      ]  # also, major tm
  cLabels = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,
             0.7,0.8,0.9,0.95,0.99,1.0      ]
  rad     = 4. * numpy.arctan(1.0) / 180.
  angC    = numpy.arccos(cLabels) / rad                       # angles: correlation labels
                                                                       
  if (rOpts and hasattr(rOpts,"tiMainString")) :
      rxy.tiMainString      = rOpts.tiMainString
      if (hasattr(rOpts,"tiMainFontHeightF")) :
           rxy.tiMainFontHeightF = rOpts.tiMainFontHeightF
  else :
           rxy.tiMainFontHeightF = 0.0225              # default  0.025              

  taylor = xy(wks,xx,yy,rxy)                       # Create and draw XY plot.

  rsrRes  = Resources()
  rsrRes.gsLineThicknessF  = rxy.xyLineThicknesses[0]  # line thickness
  rsrRes.gsLineDashPattern = 0                         # solid line pattern
                                                       # draw x and y to xyMax
  dum0 = add_polyline(wks,taylor, [0.,  0.], [0.,xyMax], rsrRes)
  dum1 = add_polyline(wks,taylor, [0.,xyMax], [0.,  0.], rsrRes)

  xx   = numpy.linspace(xyMin, xyOne ,npts)               # draw 1.0 standard radius
  yy   = numpy.sqrt(xyOne - xx**2)   
  rsrRes.gsLineDashPattern = 1                         # dashed line pattern
  rsrRes.gsLineThicknessF  = rxy.xyLineThicknesses[0]  # line thickness
  dum2 = add_polyline(wks,taylor,xx,yy, rsrRes)
  del xx
  del yy
                               
  if (rOpts and hasattr(rOpts,"stnRad") ) :
      rsrRes.gsLineThicknessF  = 1                     # rxy.xyLineThicknesses[0]
      nStnRad = numpy.size(rOpts.stnRad)

      dum3  = []
      for n in range(nStnRad):
         rr = rOpts.stnRad[n]
         xx = numpy.linspace(xyMin, rr ,npts) 
         yy = numpy.sqrt(rr**2   - xx**2)   
         dum3.append(add_polyline(wks,taylor,xx,yy, rsrRes))

      del xx
      del yy

  tmYLLabelFont = get_integer(taylor, "tmYLLabelFont")
  tmYLLabelFontHeightF = get_integer(taylor, "tmYLLabelFontHeightF")

# ----------------------------------------------------------------
# Part 2:
# Correlation labels
# ----------------------------------------------------------------
  radC    = xyMax                                 # for correlation labels
  xC      = radC * numpy.cos(angC*rad)
  yC      = radC * numpy.sin(angC*rad)
  xC      = xC + 0.020 * numpy.cos(rad*angC)         # added to get some separation
  yC      = yC + 0.060 * numpy.sin(rad*angC)

  txRes               = Resources()           # text mods desired
  txRes.txFontHeightF = FontHeightF               # match YL 
  txRes.tmYLLabelFont = tmYLLabelFont             # match YL
  txRes.txAngleF      = -45.
  if ( not hasattr(rOpts, "drawCorLabel") or rOpts.drawCorLabel) : 
      dum4 = add_text(wks,taylor,"Correlation",1.30,1.30,txRes)
  txRes.txAngleF      = 0.0 
  txRes.txFontHeightF = FontHeightF*0.50          # bit smaller

  plRes               = Resources()
  plRes.gsLineThicknessF = 2.
  txRes.txJust        = "CenterLeft"              # Default="CenterCenter".
  txRes.txFontHeightF = FontHeightF               # match YL 
  tmEnd = 0.975
  radTM = xyMax*tmEnd                             # radius end: major TM 
  xTM   = numpy.zeros( 2 , dtype=float)
  yTM   = numpy.zeros( 2 , dtype=float)

  dum5 = []
  dum6 = []
  for i in range(numpy.size(sLabels)):               # Loop to draw strings
    txRes.txAngleF = angC[i]
    dum5.append(add_text(wks, taylor, sLabels[i],xC[i],yC[i],txRes))   # cor label
    xTM[0]   = xyMax * numpy.cos(angC[i]*rad)        # major tickmarks at
    yTM[0]   = xyMax * numpy.sin(angC[i]*rad)        # correlation labels
    xTM[1]   = radTM * numpy.cos(angC[i]*rad)             
    yTM[1]   = radTM * numpy.sin(angC[i]*rad)
    dum6.append(add_polyline(wks,taylor,xTM,yTM,plRes))
                                                  # minor tm locations
  mTM     = [0.05,0.15,0.25,0.35,0.45,0.55,0.65,
             0.75,0.85,0.91,0.92,0.93,0.94,0.96,0.97,0.98  ]
  angmTM  = numpy.arccos(mTM)/rad                    # angles: correlation labels
  radmTM  = xyMax*(1.-(1.-tmEnd)*0.5)             # radius end: minor TM 

  dum7 = []
  for i in range(numpy.size(mTM)):                   # manually add tm
    xTM[0]   = xyMax * numpy.cos(angmTM[i]*rad)      # minor tickmarks
    yTM[0]   = xyMax * numpy.sin(angmTM[i]*rad)
    xTM[1]   = radmTM * numpy.cos(angmTM[i]*rad)          
    yTM[1]   = radmTM * numpy.sin(angmTM[i]*rad)
    dum7.append(add_polyline(wks,taylor,xTM,yTM,plRes))
                                                  # added for Wanli
  if ( rOpts and hasattr(rOpts, "ccRays") ) :
      angRL = numpy.arccos(rOpts.ccRays)/rad         # angles: radial lines

      rlRes = Resources()
      rlRes.gsLineDashPattern= 2                  # line pattern
      rlRes.gsLineThicknessF = 1                  # choose line thickness
      if (hasattr(rOpts, "ccRays_color")) :
        rlRes.gsLineColor = rOpts.ccRays_color
      else :
        rlRes.gsLineColor    =  "black"

      dum8 = []
      for i in range(numpy.size(angRL)):
         xRL     = xyMax * numpy.cos(angRL[i]*rad)
         yRL     = xyMax * numpy.sin(angRL[i]*rad)
         dum8.append(add_polyline(wks,taylor, [0, xRL], [0,  yRL], rlRes))


# ----------------------------------------------------------------
# Part 3:
# Concentric about 1.0 on XB axis
# I think this is correct. Still test mode.
# ----------------------------------------------------------------
  if (rOpts and hasattr(rOpts,"centerDiffRMS") and rOpts.centerDiffRMS) :
      respl                    = Resources()     # polyline mods desired
      respl.gsLineThicknessF   = 1.0                 # line thickness
      respl.gsLineDashPattern  = 2                   # short dash lines
      respl.gsLineColor        = "black"             # line color     
      if (hasattr(rOpts,"centerDiffRMS_color")) :
          respl.gsLineColor    =  rOpts.centerDiffRMS_color

      dx   = 0.25
      ncon = 4                                       # 0.75, 0.50, 0.25, 0.0
      npts = 100                                     # arbitrary
      ang  = numpy.linspace(180,360,npts)*rad

      dum9 = []

      for n in range(ncon+1):
         rr  = n*dx                                  # radius from 1.0 [OBS] abscissa
         xx  = 1. + rr * numpy.cos(ang)
         yy  = abs( rr * numpy.sin(ang) )
         if (n <= 2) :
             dum9.append(add_polyline(wks,taylor,xx,yy,respl))
         if (n == 3) :
             n3 = int( 0.77*npts )
             dum9.append(add_polyline(wks,taylor,xx[0:n3+1],yy[0:n3+1],respl))
         if (n == 4) :
             n4 = int( 0.61*npts )
             dum9.append(add_polyline(wks,taylor,xx[0:n4+1],yy[0:n4+1],respl))
	     
      del ang
      del xx
      del yy


# ---------------------------------------------------------------
# Part 4:
# generic resources that will be applied to all users data points
# of course, these can be changed 
# http://www.ncl.ucar.edu/Document/Graphics/Resources/gs.shtml
# ---------------------------------------------------------------
  if (rOpts and hasattr(rOpts,"Markers")) :
      Markers = rOpts.Markers
  else :
      Markers = [ 4, 6, 8,  0, 9, 12, 7, 2, 11, 16]  # Marker Indices

  if (rOpts and hasattr(rOpts,"Colors")) :
      Colors  = rOpts.Colors
  else :
      Colors  = [ "red", "blue", "green", "cyan", "orange",
                  "torquoise", "brown", "yellow", "purple", "black"]

  if (rOpts and hasattr(rOpts,"gsMarkerThicknessF")) :
      gsMarkerThicknessF = rOpts.gsMarkerThicknessF
  else :
      gsMarkerThicknessF = 1.0

  if (rOpts and hasattr(rOpts,"gsMarkerSizeF")) :
      gsMarkerSizeF      = rOpts.gsMarkerSizeF
  else :
      gsMarkerSizeF      = 0.0085                    # Default: 0.007

  gsRes = Resources()
  gsRes.gsMarkerThicknessF = gsMarkerThicknessF      # default=1.0
  gsRes.gsMarkerSizeF      = gsMarkerSizeF           # Default: 0.007 

  ptRes = Resources()                            # text options for points
  ptRes.txJust             = "BottomCenter"          # Default="CenterCenter".
  ptRes.txFontThicknessF   = 1.2                     # default=1.00
  ptRes.txFontHeightF      = 0.0125                  # default=0.05
  if (rOpts and hasattr(rOpts,"txFontHeightF")) :
      ptRes.txFontHeightF  = rOpts.txFontHeightF

  markerTxYOffset          = 0.0175                  # default
  if (rOpts and hasattr(rOpts,"markerTxYOffset")) :
      markerTxYOffset = rOpts.markerTxYOffset        # user defined offset

  dum10 = []
  dum11 = []

  for n in range(nCase):
     gsRes.gsMarkerIndex   = Markers[n]              # marker style (+)
     gsRes.gsMarkerColor   = Colors[n]               # marker color
     ptRes.txFontColor     = gsRes.gsMarkerColor
     for i in range(nVar) :
       dum10.append(add_polymarker(wks,taylor,X[n,i],Y[n,i],gsRes))
       print ('X(n,i) = %f  Y(n,i) = %f' %(X[n,i], Y[n,i]))
       dum11.append(add_text(wks,taylor,str(i+1),X[n,i],Y[n,i]+markerTxYOffset,ptRes))


# ---------------------------------------------------------------
# Part 5: # add case legend and variable labels
# ---------------------------------------------------------------

#  if (rOpts and hasattr(rOpts,"caseLabels")) : 

#      if (hasattr(rOpts,"caseLabelsFontHeightF")) :
#          caseLabelsFontHeightF = rOpts.caseLabelsFontHeightF
#      else :
#          caseLabelsFontHeightF = 0.05  

#      lgres                    = Resources()
#      lgres.lgMarkerColors     = Colors        # colors of markers
#      lgres.lgMarkerIndexes    = Markers       # Markers 
#      lgres.lgMarkerSizeF      = gsMarkerSizeF # Marker size
#      lgres.lgItemType         = "Markers"     # draw markers only
#      lgres.lgLabelFontHeightF = caseLabelsFontHeightF  # font height of legend case labels

#      if (hasattr(rOpts,"legendWidth")) :
#          lgres.vpWidthF       = rOpts.legendWidth
#      else :
#          lgres.vpWidthF       = 0.15          # width of legend (NDC)

#      if (hasattr(rOpts,"legendHeight")) :
#          lgres.vpHeightF      = rOpts.legendHeight
#      else :
#          lgres.vpHeightF      = 0.030*nCase   # height of legend (NDC)

#      lgres.lgPerimOn          = False         # turn off perimeter
#      nModel                   = numpy.size( rOpts.caseLabels )
#      print nModel, rOpts.caseLabels
#      lbid = legend_ndc(wks,nModel,rOpts.caseLabels,0.35,-0.35,lgres)
	 
  if (rOpts and hasattr(rOpts,"caseLabels")) : 
    nCase    = numpy.size(rOpts.caseLabels)
      
    if (hasattr(rOpts,"caseLabelsFontHeightF")) :
      caseLabelsFontHeightF = rOpts.caseLabelsFontHeightF
    else :
      caseLabelsFontHeightF = 0.05 

      txres = Resources()
      txres.txFontHeightF = caseLabelsFontHeightF
      txres.txJust = "CenterLeft"              # justify to the center left

      delta_y = 0.1   
      delta_x = 0.05  
      if (rOpts and hasattr(rOpts,"caseLabelsXloc")) :
          xs  = rOpts.caseLabelsXloc            # user specified
      else :
          xs  = 1.                
      
      if (rOpts and hasattr(rOpts,"caseLabelsYloc")) :
          ys  = rOpts.caseLabelsYloc            # user specified
      else :
          ys  = max( [nCase*delta_y , 0.30]) 
	  
      gsres               = Resources()
      gsres.gsMarkerSizeF = gsMarkerSizeF
      
      for i in range(nCase):     
         if (i==0) :
             dum12 = []
             dum13 = []
	     
         gsres.gsMarkerColor	 = Colors[i]	 # colors of markers
         gsres.gsMarkerIndex	 = Markers[i]	 # Markers 
         dum13.append(add_polymarker(wks, taylor, xs-delta_x, ys, gsres) )   # Draw a polymarker.

         txres.txFontColor     = Colors[i]        # colors of markers
         dum12.append(add_text(wks,taylor, rOpts.caseLabels[i], xs, ys, txres))
         ys = ys- delta_y
  
  if (rOpts and hasattr(rOpts,"varLabels")) : 
      nVar    = numpy.size(rOpts.varLabels)

      if (hasattr(rOpts,"varLabelsFontHeightF")) :
          varLabelsFontHeightF = rOpts.varLabelsFontHeightF
      else :
          varLabelsFontHeightF = 0.013

      txres = Resources()
      txres.txFontHeightF = varLabelsFontHeightF
      txres.txJust = "CenterLeft"              # justify to the center left

      delta_y = 0.06   
      if (rOpts and hasattr(rOpts,"varLabelsYloc")) :
          ys  = rOpts.varLabelsYloc            # user specified
      else :
          ys  = max( [nVar*delta_y , 0.30])
      
      for i in range(nVar):     
            if (i==0) :
              dum12 = []

              dum12.append(add_text(wks,taylor, str(i+1) + " - " + rOpts.varLabels[i], .125,ys,txres))
              ys = ys- delta_y
  
  if (not hasattr(rOpts,"taylorDraw") or \
      (hasattr(rOpts,"taylorDraw") and rOpts.taylorDraw)) : 
	    draw(taylor)
  if (not hasattr(rOpts,"taylorFrame") or \
      (hasattr(rOpts,"taylorFrame") and rOpts.taylorFrame)) : 
      frame(wks)

  return taylor